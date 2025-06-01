from pydantic import BaseModel


class taskRequest(BaseModel):
    title:str
    description:str
    is_completed:bool
    
    class Config:
        from_attributes = True