import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from db import  init_db
from routers import auth, task, admin


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

app.include_router(auth.router)
app.include_router(task.router)
app.include_router(admin.router)



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






