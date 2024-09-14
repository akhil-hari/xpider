import asyncio
from typing import Type

from xpider.queue.queue_factory import QueueFactory
from xpider.utils.singleton import Singleton


class ProcessLoop(Singleton):
    def __init__(self):
        self.max_threads = 5
        self.loop = asyncio.get_event_loop()
        self.stop_flag = False
        self.queue = QueueFactory.create_queue()

    async def __worker_function__(self):
        while True:
            id_str, request_dict = self.queue.dequeue()
            self.queue.acknowledge(id_str)
            results = None
            async for request_or_data in results:
                if request_or_data:
                    pass

    def start(self, spider_class: Type[object]):
        pass
