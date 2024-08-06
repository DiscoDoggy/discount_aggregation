from fastapi import FastAPI
import services
from itemModel import Item
from filterModel import FilterModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

item_handler = services.ItemHandler()

@app.get("/")
async def root():
    return {"message" : "hello world, this is my backend"}

@app.get("/items", response_model = list[Item])
def get_all_items(sort_key: str | None=None):
    #unprocessed... list of elements that sqlalchemy returned
    unprocessed_items = item_handler.get_all_items(sort_key)
    items_list = []
    for item in unprocessed_items:
        items_list.append(item)

    return items_list

@app.get("/items/{gender}", response_model = list[Item])
def get_items_by_gender(gender: str, sort_key: str | None = None):
    # unprocessed... list of elements that sqlalchemy returned
    if sort_key != None:
        unprocessed_items = item_handler.get_items_by_category(gender, sort_key)
    else:
        unprocessed_items = item_handler.get_items_by_category(gender)
    
    items_list = []
    for item in unprocessed_items:
        items_list.append(item)
        print(item.rating)

    return items_list

@app.post("/items/{category}/filter", response_model=list[Item])
def get_filter_items(category: str, filterCriteria: FilterModel, sort_key: str | None=None):
    print_filter_criteria(filterCriteria)
    query_results = item_handler.query_filter_items(category, filterCriteria, sort_key)
    items_list = []
    for item in query_results:
        items_list.append(item)

    return items_list

def print_filter_criteria(filterCriteria):
    print(f"Min_price: {filterCriteria.min_price}")
    print(f"Max_price: {filterCriteria.max_price}")
    print(f"Sizes: {filterCriteria.sizes}")
    print(f"Colors: {filterCriteria.colors}")
    print(f"Ratings: {filterCriteria.ratings}")