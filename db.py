from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base

DATABASE_URL = "sqlite+aiosqlite:///./project.db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_= AsyncSession)



# initialize database for async
async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
        
async def get_db():
    async with AsyncSessionLocal() as db:
    
        try: 
            yield db
        finally:
            #db.close
            await db.close()        