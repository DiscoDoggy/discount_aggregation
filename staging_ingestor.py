from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

class StagingIngestor:
    def __init__(self):
        self.client = self.setup_client()
        
    def ingest_data(self, json_data):
        self.client.inventory.insert_many(json_data)

    def setup_client(self):
        load_dotenv()
        MONGO_USERNAME = os.getenv('MONGO_DB_USERNAME')
        MONGO_PASSWORD = os.getenv('MONGO_DB_PASSWORD')

        url = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@discount-aggregation-st.wzbylfi.mongodb.net/?retryWrites=true&w=majority&appName=discount-aggregation-staging-db'
        client = MongoClient(url,server_api=ServerApi('1'))
        
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        return client
     
