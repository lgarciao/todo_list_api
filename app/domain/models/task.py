from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]


class Task(TaskBase):
    id: UUID
    todo_list_id: UUID
    created_at: datetime
    updated_at: datetime
