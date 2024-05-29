from baseScraper import *
from constants import *

class UniqloScraper(BaseScrapper):
    def __init__(self):
        super().__init__(UNIQLO_SALES_API_EP)
        self.user_agent = super().get_random_user_agent()
        self.headers = UNIQLO_HEADER
        self.headers["User-Agent"] = self.user_agent
        self.session.headers = self.headers

    def scrape(self):

        for path_id in UNIQLO_API_PATH_PARAMS:
            #store all json responses in an array to prepare it for parsing
            pass
    
    def handle_pagination(self):
        pass

    def assemble_api_params(self):
        pass

    def test_api_run(self):
        response = self.session.get('https://www.uniqlo.com/us/api/commerce/v5/en/products?path=22210,,,&flagCodes=discount&offset=0&limit=36&httpFailure=true')
        print(f'Status Code: {response.status_code}')
        print(f'Headers: {self.session.headers}')
        # print(f'Response: {response.text}')
        print(response.json())
        print(f'response text type:{type(response.json())}')
            
