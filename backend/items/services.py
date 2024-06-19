from sqlalchemy import create_engine, MetaData, Table, insert, update, select
import os
from dotenv import load_dotenv
from pathlib import Path

def init_connection():
    load_env()
    
    POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_NAME = os.getenv('POSTGRES_NAME')

    connection_url = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
    engine = create_engine(connection_url, echo=True) 
    connection = engine.connect()
    return engine, connection
 
def load_env():
    current_dir = Path(__file__).resolve().parent
    app_dir = current_dir.parents[2]
    env_path = app_dir / '.env'

    load_dotenv(dotenv_path=env_path)