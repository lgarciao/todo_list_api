from fastapi import APIRouter, status, Depends
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.models.task import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskStatus,
    TaskPriority,
)
from app.infrastructure.db.postgres import get_db
from app.infrastructure.repositories.task_repository import TaskRepository
from app.application.use_cases.task_use_case import TaskUseCase
from app.infrastructure.repositories.todo_list_repository import ToDoListRepository

router = APIRouter(prefix="/todo-lists/{list_id}/tasks", tags=["Tasks"])


def get_task_repository(db: Session = Depends(get_db)):
    return TaskRepository(db)


def get_todo_list_repository(db: Session = Depends(get_db)):
    return ToDoListRepository(db)


def get_task_use_case(
    task_repository: TaskRepository = Depends(get_task_repository),
    todo_list_repository: ToDoListRepository = Depends(get_todo_list_repository),
):
    return TaskUseCase(task_repository, todo_list_repository)


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    list_id: UUID, data: TaskCreate, use_case: TaskUseCase = Depends(get_task_use_case)
):
    return use_case.create_task(list_id, data)


@router.get("/", response_model=List[Task])
def list_tasks(
    list_id: UUID,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    return use_case.list_tasks(list_id, status, priority)


@router.get("/{task_id}", response_model=Task)
def get_task(
    list_id: UUID, task_id: UUID, use_case: TaskUseCase = Depends(get_task_use_case)
):
    return use_case.get_task(list_id, task_id)


@router.put("/{task_id}", response_model=Task)
def update_task(
    list_id: UUID,
    task_id: UUID,
    data: TaskUpdate,
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    return use_case.update_task(list_id, task_id, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    list_id: UUID, task_id: UUID, use_case: TaskUseCase = Depends(get_task_use_case)
):
    use_case.delete_task(list_id, task_id)
    return None


@router.patch("/{task_id}/status", response_model=Task)
def change_status(
    list_id: UUID,
    task_id: UUID,
    status: TaskStatus,
    use_case: TaskUseCase = Depends(get_task_use_case),
):
    return use_case.change_status(list_id, task_id, status)


@router.get("/completion-percentage", response_model=float)
def get_completion_percentage(
    list_id: UUID, use_case: TaskUseCase = Depends(get_task_use_case)
):
    return use_case.get_completion_percentage(list_id)
