import requests
from baseScraper import *
from uniqlo_json_processor import *
from uniqlo_scraper import *
from constants import *
import json
import pandas as pd

class StoreDriver:
    def __init__(self, store_scraper:BaseScrapper, json_processor : JsonProcessor | None):
        self.store_scraper = store_scraper
        self.json_processor = json_processor
    
    def run(self):

        json_item_list = []
        unprocessed_json_item_info = self.store_scraper.scrape()
        
        for json_item in unprocessed_json_item_info:
            if self.json_processor != None:
                processed_json_list = self.json_processor.parse_json(json_item)

                for obj in processed_json_list:
                    json_item_list.append(obj)
        
        
        #ingest the data or write it to a file or something for now.
        
        #detect if we are dealing with a batch or a singular item to push to the db
        

    def test_write_to_file(self, json_object):
        file_obj = open('test.json', 'a')
        
        writeable_json = json.dumps(json_object, indent=4)
        file_obj.write(writeable_json)
        
        file_obj.close()

def main():
    scraping_object = UniqloScraper()
    parsing_object = UniqloJsonProcessor()
    driver_object = StoreDriver(scraping_object, parsing_object)
    #ingestion object, all items from the returned obojet
    driver_object.run()

main()
