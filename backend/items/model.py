from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

class Item(BaseModel):
    name : str
    base_price : float
    promo_price : float | None = None
    gender : str
    colors : list[str]
    sizes : list[str]
    rating : float | None = None 
    num_ratings : int | None = None
    sale_start : date | None = None
    image_links : list[str]
    link : str
    site_name : str | None=None
