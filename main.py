from unittest.mock import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, String, Boolean




 
app = FastAPI() 

app.add_middleware(
    CORSMiddleware
)

database_url = "sqlite.////"

# #path parameter
# @app.get("/{name}")
# def index(name:str):
#     return {"message":f"Hello World !, {name}"}

# query parameter - day & phone
@app.get("/{name}")
def index(name:str, day:str, phone:str):
    return(f"{name}, {day}, {phone}")

class Task(Base):
    __table__ = "tasks"
    id = Column(String)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean)

