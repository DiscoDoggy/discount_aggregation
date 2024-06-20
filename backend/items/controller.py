from fastapi import FastAPI
import services
from model import Item

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

@app.get("/items/{gender}", response_model = list[Item])
def get_items_by_gender(gender: str):
    # unprocessed... list of elements that sqlalchemy returned
    unprocessed_items = item_handler.get_items_by_gender(gender)
    items_list = []
    for item in unprocessed_items:
        items_list.append(item)

    return items_list