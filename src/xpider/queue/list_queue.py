from typing import Tuple

from xpider.queue.base_queue import BaseQueue
from xpider.utils.singleton import Singleton


class ListQueue(BaseQueue, Singleton):
    def __init__(self, settings: dict):
        self.__queue__ = []
        self.__no_ack_set__ = set()

    def enqueue(self, obj: dict):
        self.__queue__.append(obj)

    def dequeue(self) -> Tuple[str, dict]:
        item: dict = self.__queue__.pop(0)
        id_str = item.get("requestId", "")
        # print("id-str", id_str)
        self.__no_ack_set__.add(id_str)
        return id_str, item

    def acknowledge(self, id_str: str):
        # print("\nacktry ", id_str)
        self.__no_ack_set__.remove(id_str)

    def empty(self) -> bool:
        return len(self.__queue__) == 0

    def has_unprocessed(self) -> bool:
        return len(self.__no_ack_set__) > 0
