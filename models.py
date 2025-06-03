from sqlalchemy import Column, String, Boolean,Integer
from db import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority=Column(Integer)
    is_completed = Column(Boolean, default=False)