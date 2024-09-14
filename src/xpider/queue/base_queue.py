from abc import ABC, abstractmethod
from typing import Tuple


class BaseQueue(ABC):
    @abstractmethod
    def enqueue(self, obj: dict):
        pass

    @abstractmethod
    def dequeue(self) -> Tuple[str, dict]:
        pass
 
    @abstractmethod
    def acknowledge(self, id_str: str):
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass

    @abstractmethod
    def has_unprocessed(self) -> bool:
        pass
