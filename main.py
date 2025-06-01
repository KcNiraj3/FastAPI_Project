import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, String, Boolean,Integer, create_engine
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from typing import List
from fastapi import HTTPException

from db import AsyncSessionLocal, init_db
from requests_models import taskRequest
from response_models import TaskResponse
from models import Task
from fastapi import APIRouter
from route import router


# #path parameter
# @app.get("/{name}")
# def index(name:str):
#     return {"message":f"Hello World !, {name}"}

# query parameter - day & phone
# @app.get("/{name}")
# def index(name:str, day:str, phone:str):
#     return(f"{name}, {day}, {phone}")


#router = APIRouter(prefix="/api")
app = FastAPI() 
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    #ALLOW_METHODS=["GET"]
)

app.include_router(router)



# after app is created start
@app.on_event("startup")
async def on_startup():
    await init_db()
    



# pydantic model for validation , pydantic also convert into json
# Request for input -for put and post

    
# For output - get method , send data to client    
  

templates = Jinja2Templates(directory="templates")

@app.get("/web", response_class=HTMLResponse)
def _web(request: Request):
    return templates.TemplateResponse("web.html", {"request": request})

@app.get("/list_tasks", response_class=HTMLResponse)
def web(request: Request):
    return templates.TemplateResponse("list_tasks.html", {"request": request})



# #one task
# @app.post("/tasks/")  
# def create_tasks(task:taskRequest, db: Session = Depends(get_db)):
#     db_task = Task(**task.dict())
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return db_task   



