import asyncio
from typing import Type, Union, Iterator, AsyncIterator, Any
import time

from xpider.queue.queue_factory import QueueFactory
from xpider.data_gatherer.data_gatherer_factory import DataGathererFactory
from xpider.utils.singleton import Singleton
from xpider.http.http_request import Request
from xpider.processor.multi_runner_lock import MultiRunnerLock

from logging import getLogger
from pydantic import BaseModel


logger = getLogger("xpider-network-logs")


class ProcessLoop(Singleton):
    def __init__(self, spider_class:Type[object], settings:dict):
    # def __init__(self, spider_class: Type[object]):
        if not hasattr(spider_class, "start_crawl"):
            raise AttributeError("No `start_crawl` method defined in spider class")
        self.settings = settings
        self.name = settings.get("name")
        self.max_threads = settings.get("threads", 5)
        self.max_retry = settings.get("max_retry", 20)
        self.proxy = settings.get("proxy")
        self.loop = asyncio.get_event_loop()
        self.stop_flag = False
        self.queue = QueueFactory.create_queue(settings)
        self.spider_object = spider_class()
        self.data_gatherer = DataGathererFactory.create_data_gatherer(settings)
        setattr(self.spider_object, "process_loop", self)
        setattr(self.spider_object, "settings", settings)
        setattr(self.spider_object, "logger", getLogger("xpider-callback-logs"))

    async def __worker_function__(self):
        while True:
            if not self.queue.empty():
                id_str, request_dict = self.queue.dequeue()
                request = Request.from_json(request_dict)
                retry_flag = False
                logger.error(f"Sending [{request.method.upper()}] {request.url}")
                try:
                    request_start_time = time.time()
                    response = await request.send()
                    if request.callback is not None:
                        callback_fn = getattr(self.spider_object, request.callback)
                        results = callback_fn(response)
                        self.process_results(results)
                except Exception as e:
                    logger.error(e)
                    if request.retry < self.max_retry:
                        request.retry += 1
                        retry_flag = True

                
                if retry_flag:
                    request_json = request.to_json()
                    request_json.pop("requestId")
                    self.queue.enqueue(request_json)
                    self.queue.acknowledge(id_str)
                    continue
                else:
                    self.queue.acknowledge(id_str)
                request_end_time = time.time()
                logger.error(
                    f"Processed [{request.method}/{response.status_code}] {request.url} in {format(request_end_time -  request_start_time, '.2f')}s"
                )
            elif self.queue.has_unprocessed():
                await asyncio.sleep(1)
                continue
            else:
                break

    def process_results_sync(self, results: Iterator[Request | BaseModel]):
        for request_or_data in results:
            if isinstance(request_or_data, Request):
                request_or_data.add_request_id()
                self.queue.enqueue(request_or_data.to_json())
            elif isinstance(request_or_data, BaseModel):
                self.data_gatherer.write(
                    request_or_data.__class__.__name__, request_or_data
                )

    async def process_results_async(self, async_results: AsyncIterator[Any]):
        results = []
        async for item in async_results:
            results.append(item)
        self.process_results(iter(results))

    def process_results(self, results: Union[Iterator[Any], AsyncIterator[Any]]):
        if isinstance(results, AsyncIterator):  # Type narrowing for AsyncIterator
            self.loop.create_task(self.process_results_async(results))
        elif isinstance(results, Iterator):  # Type narrowing for Iterator
            self.process_results_sync(results)
        else:
            raise TypeError("results must be an Iterator or AsyncIterator")

    def start(self):
        # self.queue.enqueue(request.to_json())
        # self.process_results(self.spider_object.start_crawl())
        with MultiRunnerLock(self.spider_object):
            tasks = []
            for _ in range(self.max_threads):
                task = self.loop.create_task(self.__worker_function__())
                tasks.append(task)
            all_workers = asyncio.gather(*tasks)
            self.loop.run_until_complete(all_workers)
