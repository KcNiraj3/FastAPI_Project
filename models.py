from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean,Integer, create_engine

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)