from uuid import UUID
from typing import List
from app.domain.models.todo_list import ToDoListCreate, ToDoListUpdate, ToDoList
from app.domain.exceptions.custom_exceptions import ToDoListNotFoundException
from app.domain.repositories.todo_list_repository_interface import (
    ToDoListRepositoryInterface,
)


class ToDoListUseCase:
    def __init__(self, repository: ToDoListRepositoryInterface):
        self.repository = repository

    def create_list(self, data: ToDoListCreate) -> ToDoList:
        return self.repository.create(data)

    def get_list(self, list_id: UUID) -> ToDoList:
        todo_list = self.repository.get_by_id(list_id)
        if not todo_list:
            raise ToDoListNotFoundException(str(list_id))
        return todo_list

    def update_list(self, list_id: UUID, data: ToDoListUpdate) -> ToDoList:
        updated = self.repository.update(list_id, data)
        if not updated:
            raise ToDoListNotFoundException(str(list_id))
        return updated

    def delete_list(self, list_id: UUID) -> None:
        if not self.repository.delete(list_id):
            raise ToDoListNotFoundException(str(list_id))

    def list_all(self) -> List[ToDoList]:
        return self.repository.list_all()
