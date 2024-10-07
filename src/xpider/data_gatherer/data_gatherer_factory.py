from xpider.data_gatherer.csv_data_gatherer import CSVDataGatherer
from xpider.data_gatherer.mongodb_data_gatherer import MongoDBDataGatherer


class DataGathererFactory:
    @staticmethod
    def create_data_gatherer(settings: dict):
        data_gatherer_type = "default"
        data_gatherer_type = (
            "mongo" if settings.get("mongo_url") is not None else data_gatherer_type
        )
        impl_map = {"mongo": MongoDBDataGatherer, "default": CSVDataGatherer}
        return impl_map[data_gatherer_type](settings)
