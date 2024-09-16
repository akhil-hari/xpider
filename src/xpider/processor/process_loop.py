import asyncio
from typing import Type,Union, Iterator, AsyncIterator, Any
import time

from xpider.queue.queue_factory import QueueFactory
from xpider.data_gatherer.data_gatherer_factory import DataGathererFactory
from xpider.utils.singleton import Singleton
from xpider.http.http_request import Request

from logging import getLogger
from pydantic import BaseModel


logger = getLogger("xpider-network-logs")


class ProcessLoop(Singleton):
    # def __init__(self, spider_class:Type[object], settings:dict):
    def __init__(self, spider_class:Type[object]):
        self.max_threads = 5
        self.loop = asyncio.get_event_loop()
        self.stop_flag = False
        self.queue = QueueFactory.create_queue()
        self.spider_object = spider_class()
        self.data_gatherer = DataGathererFactory.create_data_gatherer()
        setattr(self.spider_object ,"logger", getLogger("xpider-callback-logs"))

    async def __worker_function__(self):
        while True:
            if not self.queue.empty():
                id_str, request_dict = self.queue.dequeue()
                request = Request.from_json(request_dict)
                retry_flag = False
                logger.error(f"Sending [{request.method.upper()}] {request.url}")
                try:
                    request_start_time =  time.time()
                    response = await request.send()
                    if  request.callback is not None:
                        callback_fn = getattr(self.spider_object, request.callback)
                        results = callback_fn(response)
                        await self.process_results(results)
                except Exception:
                    if request.retry < self.max_retry():
                        request.retry += 1
                        retry_flag =  True

                self.queue.acknowledge(id_str)
                if retry_flag:
                    self.queue.enqueue(request.to_json())
                    continue
                request_end_time =  time.time()
                logger.error(f"Processed [{request.method}/{response.status_code}] {request.url} in {request_end_time -  request_start_time}s")
            elif self.queue.has_unprocessed():
                await asyncio.sleep(1)
                continue 
            else:
                break
    
    def process_results_sync(self, results:Iterator[Request| BaseModel]):
        for request_or_data in results:
            if isinstance(request_or_data, Request):
                request_or_data.add_request_id()
                self.queue.enqueue(request_or_data.to_json())
            elif isinstance(request_or_data, BaseModel):
                self.data_gatherer.write(request_or_data.__class__.__name__, request_or_data)
                
    def test(self):
        class Akhil(BaseModel):
            num:int
        
        for i in range(10):
            data = Akhil(num=i)
            yield data
            request = Request(f"https://httpbin.org/{i}")
            yield request
    
    async def process_results_async(self, async_results:AsyncIterator[Any]):
        results = []
        async for item in async_results:
            results.append(item)
        self.process_results(self.test())
    

    def process_results(self, results:Union[Iterator[Any], AsyncIterator[Any]]):
        if isinstance(results, AsyncIterator):  # Type narrowing for AsyncIterator
            self.loop.create_task(self.process_results_async(results))
        elif isinstance(results, Iterator):  # Type narrowing for Iterator
            self.process_results_sync(results)
        else:
            raise TypeError("results must be an Iterator or AsyncIterator")

        

    def start(self):
        self.process_results(self.test())
        
        # self.queue.enqueue(request.to_json())
        tasks = []
        for i in range(self.max_threads):
            task  = self.loop.create_task(self.__worker_function__())
            tasks.append(task)
        all_workers =  asyncio.gather(*tasks)
        self.loop.run_until_complete(all_workers)

        
