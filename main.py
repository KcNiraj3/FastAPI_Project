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
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///./project.db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_= AsyncSession)
Base = declarative_base()


# initialize database for async
async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


# #path parameter
# @app.get("/{name}")
# def index(name:str):
#     return {"message":f"Hello World !, {name}"}

# query parameter - day & phone
# @app.get("/{name}")
# def index(name:str, day:str, phone:str):
#     return(f"{name}, {day}, {phone}")

# model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)

app = FastAPI() 
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware
)

async def get_db():
    async with AsyncSessionLocal() as db:
    
        try: 
            yield db
        finally:
            #db.close
            await db.close()

# after app is created start
@app.on_event("startup")
async def on_startup():
    await init_db()
    



# pydantic model for validation , pydantic also convert into json
# Request for input -for put and post
class taskRequest(BaseModel):
    title:str
    description:str
    is_completed:bool
    
# For output - get method , send data to client    
class TaskResponse(BaseModel):
    id: int = None #  If no value is provided, it will default to None
    title:str = None
    description:str = None
    is_completed: bool = None    

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

# create more than one task
@app.post("/tasks/", response_model=list[taskRequest])  
async def create_tasks(tasks:list[taskRequest], db: AsyncSession = Depends(get_db)):
    task_obj = [] # create task obj for async
    for db_task in tasks:
        db_task = Task(**db_task.dict())
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        task_obj.append(db_task) # add in database
    return task_obj   


#To get all tasks
@app.get("/tasks/all") 
#@app.get("/tasks/all", response_model=List[TaskSchema]) 
async def getAll_tasks( session: AsyncSession = Depends(get_db)):
    #tasks = await db.query(Task).all() #select * from tasks
    result = await session.execute(select(Task))
    tasks = result.scalars().all() # convert into data (reference) from object , if we do not pur scalar it will return only object
    if not tasks:
        return {"message":"Tasks not found"}
    return [i for i in tasks]

@app.get("/tasks/{task_id}", response_model=TaskResponse)  
async def get_tasks(task_id:int, session: AsyncSession = Depends(get_db)):
    _start = datetime.now()
    query1 = session.execute(
        select(Task).where(Task.id == task_id)
    )
    
    query2 = session.execute(
        select(Task)
    )
    
    # asyncio.gather starts both queries at the same time
    # saves time compared to awaiting them one by one
    query1, query2 = await asyncio.gather(
        query1,
        query2
    )
    task1 = query1.scalar()
    print(f"\n\n{query1}, {task1}")
    _end = datetime.now()
    print(f"\n\ntime_taken: {_end-_start}\n\n")
    if not task1:
        return TaskResponse()
    print(task1)
    return task1

@app.put("/tasks/{task_id}")  
async def edit_tasks(task_id:int, task:taskRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    _task = result.scalar_one_or_none()
    if not _task:
        return {"error": "Task not found"}
    _task.title = task.title
    _task.description = task.description
    _task.is_completed = task.is_completed
    db.add(_task)
    await db.commit()
    await db.refresh(_task)
    return _task

@app.delete("/tasks/{task_id}")  
async def delete_tasks(task_id:int, task:taskRequest, db: AsyncSession = Depends(get_db)):
    _task = db.query(Task).filter(Task.id==task_id).first()
    if not _task:
        return {"error": "Task not found"}

    await db.delete(_task)
    await db.commit()
    return {"message":"Task deleted sucessfully"}