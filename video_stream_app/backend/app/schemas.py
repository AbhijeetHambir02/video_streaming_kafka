from pydantic import BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    username: str
    password: str

class StoreFile(BaseModel):
    id : int
    topic : str
    file_name : str
    file_path : str
    uploaded_at : datetime
    
    model_config = ConfigDict(from_attributes=True)
