from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from starlette import status
from passlib.context import CryptContext
from db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.future import select



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
#router = APIRouter(prefix="/api")
router = APIRouter()

# create Dependecies , fetch the data and close the connection        
async def get_db():
    async with AsyncSessionLocal() as db:    
        try: 
            yield db # yield means return
        finally:
            #db.close
            await db.close() 
            
async def authenticate_user(username: str, password: str, db):
    #user = db.query(Users).filter(Users.username == username).first()
    result = await db.execute(select(Users).where(Users.username == username))
    user = result.scalars().first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user            

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user( create_user_request : CreateUserRequest, db: AsyncSession = Depends(get_db)):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )

    db.add(create_user_model)
    await db.commit()
    await db.refresh(create_user_model)
    
@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: AsyncSession = Depends(get_db)):

    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return {'access_token'}