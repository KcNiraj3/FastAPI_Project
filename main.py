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


 
app = FastAPI() 
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware
)

templates = Jinja2Templates(directory="templates")

@app.get("/web", response_class=HTMLResponse)
def _web(request: Request):
    return templates.TemplateResponse("web.html", {"request": request})

@app.get("/list_tasks", response_class=HTMLResponse)
def web(request: Request):
    return templates.TemplateResponse("list_tasks.html", {"request": request})


DATABASE_URL = "sqlite:///./project.db"
engine = create_engine(DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# #path parameter
# @app.get("/{name}")
# def index(name:str):
#     return {"message":f"Hello World !, {name}"}

# query parameter - day & phone
# @app.get("/{name}")
# def index(name:str, day:str, phone:str):
#     return(f"{name}, {day}, {phone}")

def get_db():
    db = local_session()
    try: 
        yield db
    finally:
        db.close

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean)

Base.metadata.create_all(bind=engine)

# pydantic model
class taskRequest(BaseModel):
    title:str
    description:str
    is_completed:bool

# #one task
# @app.post("/tasks/")  
# def create_tasks(task:taskRequest, db: Session = Depends(get_db)):
#     db_task = Task(**task.dict())
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return db_task   

# create more than one task
@app.post("/tasks/")  
def create_tasks(tasks:list[taskRequest], db: Session = Depends(get_db)):
    for db_task in tasks:
        db_task = Task(**db_task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    return db_task   


#To get all tasks
@app.get("/tasks/all")  
def getAll_tasks( db: Session = Depends(get_db)):
    tasks = db.query(Task).all() #select * from tasks
    if not tasks:
        return {"message":"Tasks not found"}
    return tasks

@app.get("/tasks/{task_id}")  
def get_tasks(task_id:int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id==task_id).first()
    if not task:
        return {"message":"Task not found"}
    return task

@app.put("/tasks/{task_id}")  
def edit_tasks(task_id:int, task:taskRequest, db: Session = Depends(get_db)):
    _task = db.query(Task).filter(Task.id==task_id).first()
    if not _task:
        return {"error": "Task not found"}
    _task.title = task.title
    _task.description = task.description
    _task.is_completed = task.is_completed
    db.add(_task)
    db.commit()
    db.refresh(_task)
    return _task

@app.delete("/tasks/{task_id}")  
def delete_tasks(task_id:int, task:taskRequest, db: Session = Depends(get_db)):
    _task = db.query(Task).filter(Task.id==task_id).first()
    if not _task:
        return {"error": "Task not found"}

    db.delete(_task)
    db.commit()
    return {"message":"Task deleted sucessfully"}