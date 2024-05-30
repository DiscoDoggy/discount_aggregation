from baseScraper import *
from constants import *
import math
from random import randint
from time import sleep

class UniqloScraper(BaseScrapper):
    def __init__(self):
        super().__init__(UNIQLO_SALES_API_EP)
        self.user_agent = super().get_random_user_agent()
        self.headers = UNIQLO_HEADER
        self.headers["User-Agent"] = self.user_agent
        self.session.headers = self.headers

    def scrape(self):
        """
        -For every path id, which represents Mens sales, Women sales, etc
        assemble API parameters. 
        -Uniqlo API only allows grabbing up to 100 items at a time. The API is paginated. This means within a path ID
        we also need to loop through and make sure we extract all items within all pages. To know how many items there are total within
        a single path ID, the extracted JSON provides total, offset, and count. Total is the total number of items across all pages, we can calculate
        how many iterations we should do before stopping GET requests for a particular path id
        """
        for path_id in UNIQLO_API_PATH_PARAMS:
            api_params = self.assemble_api_params(path_id)

            first_res = self.session.get(self.urls_to_scrape[0], params=api_params)

            pagination_dict = first_res.json()['result']['pagination']
            total_discounted_items = pagination_dict['total']

            num_calls_to_make = math.ceil(total_discounted_items / UNIQLO_API_PRODUCT_LIMIT_PARAM)

            for i in range(num_calls_to_make):
                sleep(randint(2,5))

                api_offset = i * UNIQLO_API_PRODUCT_LIMIT_PARAM
                api_params = self.assemble_api_params(path_id, offset=api_offset)
                response = self.session.get(self.urls_to_scrape[0], params=api_params).json()

                #figure out how i want to handle the json response
                

    def assemble_api_params(self, path_id, offset=0):
        print(type(path_id))
        concat_path_id = path_id + ",,,"
        params = {
            "path" : concat_path_id,
            "flagCodes" : "discount",
            "offset" : offset,
            "limit" : UNIQLO_API_PRODUCT_LIMIT_PARAM,
            "httpFailure" : "true"
        }

        return params

    def test_api_run(self):
        api_params = self.assemble_api_params("22210")
        response = self.session.get(self.urls_to_scrape[0], params=api_params)
        print(f'Status Code: {response.status_code}')
        print(f'Headers: {self.session.headers}')
        print(f'response text type:{type(response.json())}')
        pagination_dict = response.json()['result']['pagination']
        total = pagination_dict['total']
        offset = pagination_dict['offset']
        count = pagination_dict['count']
        print(f"Total: {total}, Offset {offset}, Count {count}")
