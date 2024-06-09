from staging_ingestor import *
from abc import abstractmethod

class BaseTransformer():
    def __init__(self):
        self.ingestion_client = StagingIngestor().setup_client()

    def get_data_to_transform(self, extraction_id):
        return self.ingestion_client.extraction_results.inventory.find({"extraction_id": extraction_id})
    
    @abstractmethod
    def transform_data(self):
        pass
    
