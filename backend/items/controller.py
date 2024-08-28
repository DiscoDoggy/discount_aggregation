from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Response

from typing import Annotated

import services
from itemModel import Item
from filterModel import FilterModel
from userModel import CreateUserModel



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

#when uesr creates an account they send a request to this backend
#need to create a createusers end point
@app.post("/user/create")
def create_account(user_info: CreateUserModel, response:Response):
    session_token = item_handler.signup(user_info.email, user_info.password)
    response.set_cookie(key="session_id", value=session_token)

    return {"message" : "Account created successfully"}
# @app.post("/user/login")
# def login(user : dict = Depends(item_handler.authenticate_user)):
#     pass
    
@app.get("/items", response_model = list[Item])
def get_all_items(limit: int, offset: int, sort_key: str | None=None):
    #unprocessed... list of elements that sqlalchemy returned
    unprocessed_items = item_handler.get_all_items(limit=limit, offset=offset, sort_key=sort_key)
    items_list = []
    for item in unprocessed_items:
        items_list.append(item)

    return items_list

@app.get("/items/search", response_model=list[Item])
def get_search_items(limit: int, offset: int, search_query : str, sort_key: str | None = None):
    print("ENTER SEARCH ITEMS")
    query_results = item_handler.query_search_items(limit=limit, offset=offset, search_query=search_query, sort_key=sort_key)
    
    items_list = []
    for item in query_results:
        items_list.append(item)
    
    return items_list

@app.get("/items/{gender}", response_model = list[Item])
def get_items_by_gender(limit: int, offset: int, gender: str, sort_key: str | None = None):
    # unprocessed... list of elements that sqlalchemy returned
    if sort_key != None:
        unprocessed_items = item_handler.get_items_by_category(limit=limit, offset=offset, category=gender, sort_key=sort_key)
    else:
        unprocessed_items = item_handler.get_items_by_category(limit=limit, offset=offset, category=gender)
    
    items_list = []
    for item in unprocessed_items:
        items_list.append(item)
        print(item.rating)

    return items_list

@app.post("/items/{category}/filter", response_model=list[Item])
def get_filter_items(limit: int, offset: int, category: str, filterCriteria: FilterModel, sort_key: str | None=None):
    print_filter_criteria(filterCriteria)
    query_results = item_handler.query_filter_items(limit, offset, category, filterCriteria, sort_key)
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