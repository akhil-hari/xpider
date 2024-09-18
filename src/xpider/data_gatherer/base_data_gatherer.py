from abc import ABC, abstractmethod

from pydantic import BaseModel

from xpider.utils.singleton import Singleton


class BaseDataGatherer(ABC, Singleton):
    @abstractmethod
    def write(self, dataset: str, data: BaseModel):
        pass
