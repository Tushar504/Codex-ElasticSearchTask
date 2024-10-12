from pydantic import BaseModel
from typing import List


class TaskCreate(BaseModel):
    title: str
    description: str

class Task(BaseModel):
    id: int
    title: str
    description: str

class TaskSearch(BaseModel):
    id: int         
    fieldName: str   
    fieldContent: str

class TaskSearchResponse(BaseModel):
    results: List[TaskSearch]