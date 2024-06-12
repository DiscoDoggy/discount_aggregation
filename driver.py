from baseScraper import *
from uniqlo_json_processor import *
from uniqlo_scraper import *
from staging_ingestor import *
from uniqlo_constants import *
from base_transformer import *
from uniqlo_transformer import *
from final_ingestor import *
import json
import uuid
import datetime

class StoreDriver:
    def __init__(self, store_scraper:BaseScrapper, json_processor : JsonProcessor | None, ingestion_object:StagingIngestor, transformer_object:BaseTransformer):
        self.store_scraper = store_scraper
        self.json_processor = json_processor
        self.ingestor = ingestion_object
        self.transformer = transformer_object

        self.extraction_id = str(uuid.uuid4())
        self.extraction_start_datetime = str(datetime.datetime.now(datetime.timezone.utc))

    def run(self):
        unprocessed_json_item_info = self.store_scraper.scrape()
        json_items_list = self.collect_data_for_ingestion(unprocessed_json_item_info)
        results = self.ingestor.ingest_data(json_items_list)
        transformed_data = self.transformer.transform_data(self.extraction_id)
        final_ingestor_object = FinalIngestor(transformed_data)
        final_ingestor_object.ingest_data()


        # print(transformed_data)


    def test_write_to_file(self, json_object):
        file_obj = open('test.json', 'a')
        
        writeable_json = json.dumps(json_object, indent=4)
        file_obj.write(writeable_json)
        
        file_obj.close()

    def collect_data_for_ingestion(self, unprocessed_json_item_info):
        json_item_list = []
        
        for json_item in unprocessed_json_item_info:
            if self.json_processor != None:
                processed_json_list = self.json_processor.parse_json(json_item)

                for obj in processed_json_list:
                    obj = self.add_info_fields_to_json(obj)
                    self.test_write_to_file(obj)
                    json_item_list.append(obj)

        return json_item_list
    
    def add_info_fields_to_json(self, json_obj):
        json_obj['extraction_id'] = self.extraction_id
        json_obj['extraction_datetime'] = self.extraction_start_datetime
        json_obj['site_id'] = self.store_scraper.get_site_id()

        return json_obj


def main():
    scraping_object = UniqloScraper()
    parsing_object = UniqloJsonProcessor()
    ingestion_object = StagingIngestor()
    transformer_object = UniqloTransformer()
    driver_object = StoreDriver(scraping_object, parsing_object, ingestion_object, transformer_object)
    driver_object.run()

main()
