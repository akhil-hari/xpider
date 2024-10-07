from pydantic import BaseModel
from xpider.data_gatherer.base_data_gatherer import BaseDataGatherer
from pymongo import MongoClient


class MongoDBDataGatherer(BaseDataGatherer):
    def __init__(self, settings: dict):
        mongo_url: str = settings.get("mongo_url", "")
        self.project_name = settings.get("name")
        self.client = MongoClient(mongo_url)
        self.db = self.client[f"xpider_{self.project_name}_db"]

    def write(self, dataset: str, data: BaseModel):
        data_dict = dict(data)
        collection = self.db[dataset]
        collection.insert_one(data_dict)
