from fastapi import FastAPI
import services
from model import Item
from sqlalchemy import RowMapping

app = FastAPI()
item_handler = services.ItemHandler()

@app.get("/")
async def root():
    return {"message" : "hello world, this is my backend"}

@app.get("/items/", response_model = list[Item])
def get_all_items():
    #unprocessed... list of elements that sqlalchemy returned
    unprocessed_items = item_handler.get_all_items()
    items_list = []
    for item in unprocessed_items:
        items_list.append(item)

    return items_list


