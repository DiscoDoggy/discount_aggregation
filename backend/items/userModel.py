from fastapi import FastAPI
from pydantic import BaseModel

class CreateUserModel(BaseModel):
    email : str
    password: str
