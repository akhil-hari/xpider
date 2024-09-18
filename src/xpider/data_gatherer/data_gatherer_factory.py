from xpider.data_gatherer.csv_data_gatherer import CSVDataGatherer


class DataGathererFactory:
    @staticmethod
    def create_data_gatherer(data_gatherer_type: str = "default"):
        impl_map = {"default": CSVDataGatherer}
        return impl_map[data_gatherer_type]()
