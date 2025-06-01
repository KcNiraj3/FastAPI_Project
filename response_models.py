

from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: int = None #  If no value is provided, it will default to None
    title:str = None
    description:str = None
    is_completed: bool = None  