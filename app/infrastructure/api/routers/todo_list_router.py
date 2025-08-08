from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from app.infrastructure.db.postgres import get_db
from app.domain.models.todo_list import ToDoListCreate, ToDoListUpdate, ToDoList
from app.application.use_cases.todo_list_use_case import ToDoListUseCase
from app.infrastructure.repositories.todo_list_repository import ToDoListRepository

router = APIRouter(prefix="/lists", tags=["ToDo Lists"])


def get_use_case(db: Session = Depends(get_db)):
    return ToDoListUseCase(ToDoListRepository(db))


@router.post("/", response_model=ToDoList)
def create_list(
    data: ToDoListCreate, use_case: ToDoListUseCase = Depends(get_use_case)
):
    return use_case.create_list(data)


@router.get("/{list_id}", response_model=ToDoList)
def get_list(list_id: UUID, use_case: ToDoListUseCase = Depends(get_use_case)):
    return use_case.get_list(list_id)


@router.put("/{list_id}", response_model=ToDoList)
def update_list(
    list_id: UUID,
    data: ToDoListUpdate,
    use_case: ToDoListUseCase = Depends(get_use_case),
):
    return use_case.update_list(list_id, data)


@router.delete("/{list_id}")
def delete_list(list_id: UUID, use_case: ToDoListUseCase = Depends(get_use_case)):
    use_case.delete_list(list_id)
    return {"message": "List deleted successfully"}


@router.get("/", response_model=List[ToDoList])
def list_all(use_case: ToDoListUseCase = Depends(get_use_case)):
    return use_case.list_all()
