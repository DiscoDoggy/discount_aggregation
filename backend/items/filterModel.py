from fastapi import FastAPI
from pydantic import BaseModel


class FilterModel(BaseModel):
    min_price : float
    max_price : float 
    sizes : list[str]
    colors : list[str] 
    ratings : list[int]

# class FilterModel:
#     def __init__(self, min_price, max_price, sizes, colors, ratings) -> None:

#         self.min_price = min_price
#         self.max_price = max_price 
#         self.sizes = sizes 
#         self.colors = colors 
#         self.ratings = ratings