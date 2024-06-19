from sqlalchemy import create_engine, MetaData, Table, insert, update, select
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.orm import aliased
# from sqlalchemy import select_from

class ItemHandler():
    def __init__(self):
        self.engine, self.connection = self.init_connection()
        self.meta_data = MetaData()
        self.items = Table("items", self.meta_data, autoload_with=self.engine)
        self.extractions = Table("extractions", self.meta_data, autoload_with=self.engine)
        self.sites = Table("sites", self.meta_data, autoload_with=self.engine)
        self.item_change_records = Table("item_change_records", self.meta_data, autoload_with=self.engine)

    def init_connection(self):
        self.load_env()
        
        POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
        POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        POSTGRES_PORT = os.getenv('POSTGRES_PORT')
        POSTGRES_NAME = os.getenv('POSTGRES_NAME')

        connection_url = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
        engine = create_engine(connection_url, echo=False) 
        connection = engine.connect()
        return engine, connection
    
    def load_env(self):
        current_dir = Path(__file__).resolve().parent
        app_dir = current_dir.parents[2]
        env_path = app_dir / '.env'

        load_dotenv(dotenv_path=env_path)

    def get_all_items(self):
        query = select(
            self.items.c.name,
            self.items.c.base_price,
            self.items.c.promo_price,
            self.items.c.gender,
            self.items.c.colors,
            self.items.c.sizes,
            self.items.c.rating,
            self.items.c.num_ratings,
            self.items.c.sale_start,
            self.items.c.image_links,
            self.items.c.link,
            self.sites.c.name.label('site_name') 
        ).select_from(self.items).join(self.sites).where(
            self.items.c.discount_status == "ACTIVE"
        )

        query_result = self.connection.execute(query)

        return query_result
    
    def get_items_by_gender(self, gender : str):
        print(gender.upper())
        query = select(
            self.items.c.name,
            self.items.c.base_price,
            self.items.c.promo_price,
            self.items.c.gender,
            self.items.c.colors,
            self.items.c.sizes,
            self.items.c.rating,
            self.items.c.num_ratings,
            self.items.c.sale_start,
            self.items.c.image_links,
            self.items.c.link,
            self.sites.c.name.label('site_name'), 
            self.items.c.discount_status
        ).select_from(self.items).join(self.sites) \
        .where(
            self.items.c.gender == f"{gender.upper()}" 
        ).where(
            self.items.c.discount_status == "ACTIVE")
        
        
        query_result = self.connection.execute(query)

        return query_result
    
# def main():
#     item_handler = ItemHandler()
#     results = item_handler.get_all_items()
#     # for row in results.mappings():
#     #     print(type(row))
#     count = 0
#     for row in results.mappings():
#         print(row)
#         print(type(row))
#         if count == 5:
#             break
#         count += 1
# main()
