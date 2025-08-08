from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class ToDoListBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ToDoListCreate(ToDoListBase):
    pass


class ToDoListUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ToDoList(ToDoListBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
