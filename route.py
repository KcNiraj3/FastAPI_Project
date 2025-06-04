from fastapi import APIRouter, Path
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db  import get_db
from models import Task
from fastapi import HTTPException
from requests_models import taskRequest
from response_models import TaskResponse
import datetime
import asyncio
from typing import List
from starlette import status

router = APIRouter(prefix="/api")

# create more than one task
@router.post("/tasks/", response_model=list[taskRequest])  
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
@router.get("/tasks/all") 
#@router.get("/tasks/all", response_model=List[TaskResponse]) 
async def getAll_tasks( session: AsyncSession = Depends(get_db)):
    #tasks = await db.query(Task).all() #select * from tasks
    result = await session.execute(select(Task))
    tasks = result.scalars().all() # convert into data (reference) from object , if we do not put scalar it will return only object
    if not tasks:
        return {"message":"Tasks not found"}
    return [i for i in tasks]


@router.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)  
async def get_tasks(task_id:int = Path(gt=0), session: AsyncSession = Depends(get_db)): # Depends is dependency injection
    _start = datetime.datetime.now()
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
    _end = datetime.datetime.now()
    print(f"\n\ntime_taken: {_end-_start}\n\n")
    if not task1:
        raise HTTPException(status_code=404, detail="Task not found")
    print(task1)
    return task1



@router.put("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)  
async def edit_tasks(task_id:int, task:taskRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    _task = result.scalar_one_or_none()
    #if _task in None:
    if not _task:
        raise HTTPException(status_code=404, detail='Tasks not found')
    _task.title = task.title
    _task.description = task.description
    _task.priority = task.priority
    _task.is_completed = task.is_completed
    db.add(_task)
    await db.commit()
    await db.refresh(_task)
    return _task


@router.delete("/tasks/{task_id}")  
async def delete_tasks(task_id:int, task:taskRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    _task =  result.scalar_one_or_none()
    if not _task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(_task)
    await db.commit()
    return {"message":"Task deleted sucessfully"}