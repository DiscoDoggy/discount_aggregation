from fastapi import FastAPI
import services
from model import Item
from sqlalchemy import MetaData, Table
from sqlalchemy import select 

app = FastAPI()
engine, connection = services.init_connection()
meta_data = MetaData()
items = Table("items", meta_data, autoload_with=engine)
extractions = Table("extractions", meta_data, autoload_with=engine)
sites = Table("sites", meta_data, autoload_with=engine)
item_change_records = Table("item_change_records", meta_data, autoload_with=engine)
@app.get("/")
async def root():
    return {"message" : "hello world, this is my backend"}

@app.get("/items/")
def get_all_items():
    query = select(
        items.c.name,
        items.c.base_price,
        items.c.promo_price,
        items.c.gender,
        items.c.colors,
        items.c.sizes,
        items.c.rating,
        items.c.num_ratings,
        items.c.sale_start,
        items.c.image_links,
        items.c.link 
    ).where(
        items.c.discount_status == "INACTIVE"
    )

    query_result = connection.execute(query)
