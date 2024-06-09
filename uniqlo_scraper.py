from baseScraper import *
from uniqlo_constants import *
import math
from random import randint
from time import sleep

class UniqloScraper(BaseScrapper):
    def __init__(self):
        super().__init__(UNIQLO_SALES_API_EP, site_id=1)
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
            print(f"Path ID: {path_id}")
            first_res = self.make_request(path_id=path_id)

            pagination_dict = first_res['result']['pagination']
            total_discounted_items = pagination_dict['total']

            print(total_discounted_items)

            num_calls_to_make = math.ceil(total_discounted_items / UNIQLO_API_PRODUCT_LIMIT_PARAM)

            for i in range(num_calls_to_make):
                api_offset = i * UNIQLO_API_PRODUCT_LIMIT_PARAM
                response = self.make_request(path_id, api_offset)

                yield response

    def make_request(self, path_id, api_offset=0):
        api_params = self.assemble_api_params(path_id, offset=api_offset)
        for i in range(UNIQLO_NUM_RETRIES):
            time_until_retry = i ** 2
            sleep(time_until_retry)
            if i == 0:
                sleep(randint(2,7))
            try:
                response = self.session.get(self.urls_to_scrape[0], params=api_params)
                response_status_code = response.status_code
                response = response.json()
                print(response_status_code)
                if response_status_code in [200, 404]:
                    break
            except requests.exceptions.Timeout as errt: #TODO: implement a retry functionality
                print(errt)
            except requests.exceptions.TooManyRedirects as e:
                raise SystemExit(e)
            except requests.exceptions.HTTPError as errh:
                raise SystemExit(errh)
            except requests.exceptions.RequestException as err:
                SystemExit(err)

        if response_status_code == 408:
            SystemExit("System Exit -- Max retries attempted after timeout")

        return response

    def assemble_api_params(self, path_id, offset=0):
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
