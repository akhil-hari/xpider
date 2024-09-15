import asyncio
from typing import Type

from xpider.queue.queue_factory import QueueFactory
from xpider.data_gatherer.data_gatherer_factory import DataGathererFactory
from xpider.utils.singleton import Singleton
from xpider.http.http_request import Request

from logging import getLogger
from pydantic import BaseModel


logger = getLogger("xpider-network-logs")


class ProcessLoop(Singleton):
    def __init__(self, spider_class:Type[object], settings:dict):
        self.max_threads = 5
        self.loop = asyncio.get_event_loop()
        self.stop_flag = False
        self.queue = QueueFactory.create_queue()
        self.spider_object = spider_class()
        self.data_gatherer = DataGathererFactory.create_data_gatherer()
        setattr(self.spider_object ,"logger", getLogger("xpider-callback-logs"))

    async def __worker_function__(self):
        while True:
            id_str, request_dict = self.queue.dequeue()
            request = Request.from_json(request_dict)
            callback_fn = getattr(self.spider_object, request.callback) if  request.callback is not None else None
            response = await request.send()
            results = callback_fn(response)
            async for request_or_data in results:
                if isinstance(request_or_data, Request):
                    request_or_data.add_request_id()
                    self.queue.enqueue(request_or_data.to_json())
                elif isinstance(request_or_data, BaseModel):
                    self.data_gatherer.write(request_or_data.__name__, request_or_data)
                else:
                    pass

            self.queue.acknowledge(id_str)

    def start(self):
        pass
