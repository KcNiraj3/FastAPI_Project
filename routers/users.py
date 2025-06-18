from fastapi import APIRouter, Path
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db  import get_db
from models import Task, Users
from fastapi import HTTPException
from typing import Annotated, List
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext
from pydantic import BaseModel, Field

#router = APIRouter(prefix="/api")
router = APIRouter(
    prefix='/user',
    tags=['user']
)

# dependency for validating tokens
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

#create pydantic class for user verficiation
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

#To get all tasks
@router.get("/", status_code = status.HTTP_200_OK)  
async def getA_user(user:user_dependency, session: AsyncSession = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated Failed')
    result = await session.execute(select(Users).where(Users.id == user.get("id"))) # convert into data (reference) from object , if we do not put scalar it will return only object
    return (result.scalars().all())

# change password
@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)  
async def edit_password(user:user_dependency, user_verification:UserVerification, db: AsyncSession = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated Failed')
    result = await db.execute(select(Users).where(Users.id == user.get("id")))
    user_model = result.scalar_one_or_none()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    await db.commit()
    await db.refresh(user_model)
    return user_model