from pydantic import BaseModel
from xpider.data_gatherer.base_data_gatherer import BaseDataGatherer
from pathlib import Path
from csv import DictWriter, QUOTE_ALL


class CSVDataGatherer(BaseDataGatherer):
    
    def __init__(self, settings:dict):
        pass

    def write(self, dataset: str, data: BaseModel):
        data_dict = dict(data)
        dataset_path = Path(f"{dataset}.csv")
        if not dataset_path.exists():
            with dataset_path.open("w") as csv_file:
                writer = DictWriter(
                    csv_file, fieldnames=list(data_dict.keys()), quoting=QUOTE_ALL
                )
                writer.writeheader()
                writer.writerow(data_dict)
        else:
            with dataset_path.open("a") as csv_file:
                writer = DictWriter(
                    csv_file, fieldnames=list(data_dict.keys()), quoting=QUOTE_ALL
                )
                writer.writerow(data_dict)
