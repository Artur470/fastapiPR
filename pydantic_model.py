from pydantic import BaseModel
import datetime




class Todo(BaseModel):
    todo: str
