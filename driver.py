import requests
from baseScraper import *
from uniqlo_scraper import *
from constants import *

def main():
    scraping_object = UniqloScraper()
    scraping_object.test_api_run()
main()
