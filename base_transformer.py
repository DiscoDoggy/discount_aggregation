from staging_ingestor import *
from abc import abstractmethod

class BaseTransformer():
    def __init__(self, extraction_id:str):
        self.ingestion_client = StagingIngestor().setup_client()
        self.extraction_id_to_transform = extraction_id

    def get_data_to_transform(self):
        return self.ingestion_client.extraction_results.find({"extraction_id": self.extraction_id})
    
    @abstractmethod
    def transform_data(self):
        pass
    
