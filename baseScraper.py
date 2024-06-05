from abc import ABC, abstractmethod
import requests
from uniqlo_constants import *
import random


class BaseScrapper:
    def __init__(self, urls_to_scrape, site_id):
        self.urls_to_scrape = urls_to_scrape
        self.site_id = site_id
        self.session = requests.Session()


    def get_random_user_agent(self):
        return random.choice(USER_AGENTS)
    
    def get_site_id(self):
        return self.site_id

    @abstractmethod
    def scrape(self):
        '''
        Reasoning for making this an abstract method
            * Each website that requires scraping could have a different implementation
                * eg. For one site it might suffice to reverse engineer the API and use the API call
                to get data
                * Another site might require a selenium flow to manually grab each piece of data
        '''
        pass