from sqlalchemy import create_engine, MetaData, Table, select, func, insert, update
from sqlalchemy.dialects.postgresql import TSVECTOR
import os
from dotenv import load_dotenv
from pathlib import Path
from filterModel import FilterModel
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uuid
import bcrypt
import secrets
import datetime

security = HTTPBasic()

class ItemHandler():
    def __init__(self):
        self.engine, self.connection = self.init_connection()
        self.meta_data = MetaData()
        self.items = Table("items", self.meta_data, autoload_with=self.engine)
        self.extractions = Table("extractions", self.meta_data, autoload_with=self.engine)
        self.sites = Table("sites", self.meta_data, autoload_with=self.engine)
        self.item_change_records = Table("item_change_records", self.meta_data, autoload_with=self.engine)
        self.users = Table("users", self.meta_data, autoload_with=self.engine)

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

    def signup(self, email, password):
        query = select(self.users.c.email).where(self.users.c.email == email)
        results = self.connection.execute(query)
        num_results = 0

        for _ in results:
            num_results += 1

        if num_results != 0:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail="User already registered with this email."
            )
        else:
            encrypted_password = password.encode()
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(encrypted_password, salt)

            hash = hash.decode()

            session_token = self.create_new_user(email,hash)
            return session_token
        
    def authenticate_user(self, credentials:HTTPBasicCredentials=Depends(security)):
        query = select(
            self.users.c.email,
            self.users.c.password,
            self.users.c.session_token,
            self.users.c.session_end
        ).where(self.users.c.email == credentials.username)

        results = self.connection.execute(query)

        results_len = 0
        for row in results:
            pwd_in_db = row.password
            session_token = row.session_token
            session_end = row.session_end

            results_len += 1

        print(f'results_len: {results_len}')

        if results_len == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There is no account associated with this email",
                headers={"WWW-Authenticate" : "Basic"}
            )
        
        print(f'pwd_in_db: {pwd_in_db}')

        cred_encoded_pwd = credentials.password.encode()
        db_encoded_pwd = pwd_in_db.encode()

        do_passwords_match = bcrypt.checkpw(cred_encoded_pwd, db_encoded_pwd)

        if not do_passwords_match:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
        
        current_time = datetime.datetime.now()
        if session_end <= current_time:
            new_session_token, new_session_start, new_session_end = self.generate_session_token_info()

            update_session_query = update(self.users) \
                .where(self.users.c.email == credentials.username) \
                .values(
                    session_token=new_session_token,
                    session_start=new_session_start,
                    session_end=new_session_end
                )
            
            self.connection.execute(update_session_query)
            self.connection.commit()

            return new_session_token
    
        return session_token

    def create_new_user(self, email, hashed_password):
        session_token, session_start, session_end = self.generate_session_token_info()

        formatted_session_start = session_start.strftime('%Y-%m-%d %H:%M:%S')
        formatted_session_end = session_end.strftime('%Y-%m-%d %H:%M:%S')

        user_id = uuid.uuid4()

        insert_query = (
            insert(self.users).values(id=user_id, email=email, password=hashed_password, session_token=session_token, session_start=formatted_session_start, session_end=formatted_session_end)
        )
        print(str(insert_query.compile()))
        self.connection.execute(insert_query)
        self.connection.commit()

        return session_token
    
    def generate_session_token_info(self):
        session_token = secrets.token_hex(32)
        session_start = datetime.datetime.today()
        session_end = session_start + datetime.timedelta(days=30)

        return session_token, session_start, session_end
        
      
# def main():
#     item_handler = ItemHandler()
#     search_query = "blue women peanut shirt"
#     results = item_handler.query_search_items(search_query, sort_key=None)
#     for row in results.mappings():
#         print(row)
# main()
