from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.domain.models.todo_list import ToDoListCreate, ToDoListUpdate, ToDoList


class ToDoListRepositoryInterface(ABC):
    @abstractmethod
    def create(self, data: ToDoListCreate) -> ToDoList: ...

    @abstractmethod
    def get_by_id(self, list_id: UUID) -> ToDoList: ...

    @abstractmethod
    def update(self, list_id: UUID, data: ToDoListUpdate) -> ToDoList: ...

    @abstractmethod
    def delete(self, list_id: UUID) -> bool: ...

    @abstractmethod
    def list_all(self) -> List[ToDoList]: ...
