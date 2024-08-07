from sqlalchemy import create_engine, MetaData, Table, select, func
from sqlalchemy.dialects.postgresql import TSVECTOR
import os
from dotenv import load_dotenv
from pathlib import Path
from filterModel import FilterModel

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

    def get_all_items(self, limit: int, offset: int, sort_key:str = None):
        query = self.create_select_and_from()

        query = query.where(self.items.c.discount_status == "ACTIVE")

        if sort_key != None:
            query = self.append_sort_criteria(query, sort_key)


        query = query.offset(offset)
        query = query.limit(limit)

        query_result = self.connection.execute(query)

        return query_result
    
    def get_items_by_category(self, limit: int, offset: int, category : str, sort_key: str=None):
        query = self.create_select_and_from()

        query = query.where(self.items.c.discount_status == "ACTIVE")

        if category != "all":
            query = query.where(self.items.c.gender == f"{category.upper()}")
        
        if sort_key != None:
            query = self.append_sort_criteria(query, sort_key)

        query = query.offset(offset)
        query = query.limit(limit)

        query_result = self.connection.execute(query)

        return query_result
    
    def query_filter_items(self, limit: int, offset: int, category: str, filterCriteria:FilterModel, sort_key):
        query = self.create_select_and_from()

        query = query.where(self.items.c.discount_status == "ACTIVE")
        
        if category != "all":
            query = query.where(self.items.c.gender == f"{category.upper()}")
        if filterCriteria.min_price > 0.0:
            query = query.where(self.items.c.promo_price >= filterCriteria.min_price)
        if filterCriteria.max_price != 0.0:
            query = query.where(self.items.c.promo_price <= filterCriteria.max_price)
        if filterCriteria.sizes:
            query = query.where(self.items.c.sizes.op("&&")(filterCriteria.sizes))
        if filterCriteria.colors:
            query = query.where(self.items.c.colors.op("&&")(filterCriteria.colors))
        if filterCriteria.ratings:
            for i in range(len(filterCriteria.ratings)):
                filterCriteria.ratings[i] = round(filterCriteria.ratings[i])
            query = query.where(self.items.c.rating.in_(filterCriteria.ratings))

        query = self.append_sort_criteria(query, sort_key)

        query = query.offset(offset)
        query = query.limit(limit)
        
        print(str(query.compile()))
        print("Parameteres", query.compile().params)
        return self.connection.execute(query)

    def query_search_items(self, limit: int, offset: int, search_query: str, sort_key):
        tsvector_stmt = func.to_tsvector('english', 
                                         self.items.c.name + ' ' + 
                                         self.items.c.gender + ' ' + 
                                         func.array_to_string(self.items.c.colors, ' '))
        tsquery_stmt = func.plainto_tsquery('english', search_query)

        query = self.create_select_and_from()

        query = query.where(self.items.c.discount_status == "ACTIVE")
        query = query.where(tsvector_stmt.op('@@')(tsquery_stmt))

        query = self.append_sort_criteria(query, sort_key)

        query = query.offset(offset)
        query = query.limit(limit)

        print(str(query.compile()))
        print("Parameteres", query.compile().params)

        return self.connection.execute(query)
    
    def append_sort_criteria(self, query, sort_key):
        if sort_key == "price_l_h":
            query = query.order_by(self.items.c.promo_price.asc())
        elif sort_key == "price_h_l":
            query = query.order_by(self.items.c.promo_price.desc())
        elif sort_key == "sort_start-date":
            query = query.order_by(self.items.c.sale_start.desc())
        elif sort_key == "sort_rating":
            query = query.order_by(self.items.c.rating.desc())
        
        return query

    def create_select_and_from(self):
        return select(
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
            self.items.c.discount_status,
            func.count(self.items.c.id).over().label("num_total_items")
        ).select_from(self.items).join(self.sites)
        
# def main():
#     item_handler = ItemHandler()
#     search_query = "blue women peanut shirt"
#     results = item_handler.query_search_items(search_query, sort_key=None)
#     for row in results.mappings():
#         print(row)
# main()
