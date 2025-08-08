from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.models.task import (
    TaskCreate,
    TaskUpdate,
    Task,
    TaskStatus,
    TaskPriority,
)


class TaskRepositoryInterface(ABC):
    @abstractmethod
    def create(self, list_id: UUID, data: TaskCreate) -> Task: ...

    @abstractmethod
    def get_by_id(self, list_id: UUID, task_id: UUID) -> Task: ...

    @abstractmethod
    def update(self, list_id: UUID, task_id: UUID, data: TaskUpdate) -> Task: ...

    @abstractmethod
    def delete(self, list_id: UUID, task_id: UUID) -> bool: ...

    @abstractmethod
    def list_by_filters(
        self,
        list_id: UUID,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[Task]: ...
