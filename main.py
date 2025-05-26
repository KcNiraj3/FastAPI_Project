from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
app = FastAPI() 

app.add_middleware(
    CORSMiddleware
)

# #path parameter
# @app.get("/{name}")
# def index(name:str):
#     return {"message":f"Hello World !, {name}"}

# # query parameter - day & phone
# @app.get("/{name}")
# def index(name:str, day:str, phone:str):
#     return(f"{name}, {day}, {phone}")
