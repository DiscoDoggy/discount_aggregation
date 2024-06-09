from sqlalchemy import create_engine
from sqlalchemy import text 
import os
from dotenv import load_dotenv

class FinalIngestor():
    def __init__(self, processed_data:list[dict]):
        self.processed_data = processed_data
        self.engine = self.connect_to_db()
    
    def ingest_data(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT 'Hello world'"))
            print(result.all())

    def connect_to_db(self):
        load_dotenv()
        POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
        POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        POSTGRES_PORT = os.getenv('POSTGRES_PORT')
        POSTGRES_NAME = os.getenv('POSTGRES_NAME')

        connection_url = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
        engine = create_engine(connection_url, echo=True)

        return engine
    
def runner():
    mylist = [{}]
    ingestion_object = FinalIngestor(mylist)

    ingestion_object.ingest_data()

runner()

