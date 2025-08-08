from uuid import UUID
from typing import List, Optional
from app.domain.models.task import (
    TaskCreate,
    TaskUpdate,
    Task,
    TaskStatus,
    TaskPriority,
)
from app.domain.exceptions.custom_exceptions import TaskNotFoundException
from app.domain.exceptions.custom_exceptions import (
    ToDoListNotFoundException,
)
from app.domain.repositories.task_repository_interface import (
    TaskRepositoryInterface,
)
from app.domain.repositories.todo_list_repository_interface import (
    ToDoListRepositoryInterface,
)


class TaskUseCase:
    def __init__(
        self,
        task_repository: TaskRepositoryInterface,
        todo_list_repository: ToDoListRepositoryInterface,
    ):
        self.task_repository = task_repository
        self.todo_list_repository = todo_list_repository

    def create_task(self, list_id: UUID, data: TaskCreate) -> Task:
        todo_list = self.todo_list_repository.get_by_id(list_id)
        if not todo_list:
            raise ToDoListNotFoundException(str(list_id))
        return self.task_repository.create(list_id, data)

    def get_task(self, list_id: UUID, task_id: UUID) -> Task:
        task = self.task_repository.get_by_id(list_id, task_id)
        if not task:
            raise TaskNotFoundException(str(task_id))
        return task

    def update_task(self, list_id: UUID, task_id: UUID, data: TaskUpdate) -> Task:
        updated = self.task_repository.update(list_id, task_id, data)
        if not updated:
            raise TaskNotFoundException(str(task_id))
        return updated

    def delete_task(self, list_id: UUID, task_id: UUID) -> None:
        if not self.task_repository.delete(list_id, task_id):
            raise TaskNotFoundException(str(task_id))

    def change_status(self, list_id: UUID, task_id: UUID, status: TaskStatus) -> Task:
        task = self.task_repository.get_by_id(list_id, task_id)
        if not task:
            raise TaskNotFoundException(str(task_id))
        task.status = status
        return self.task_repository.update(list_id, task_id, TaskUpdate(status=status))

    def list_tasks(
        self,
        list_id: UUID,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[Task]:
        todo_list = self.todo_list_repository.get_by_id(list_id)
        if not todo_list:
            raise ToDoListNotFoundException(str(list_id))
        return self.task_repository.list_by_filters(list_id, status, priority)

    def get_completion_percentage(self, list_id: UUID) -> float:
        todo_list = self.todo_list_repository.get_by_id(list_id)
        if not todo_list:
            raise ToDoListNotFoundException(str(list_id))
        tasks = self.task_repository.list_by_filters(list_id)
        if not tasks:
            return 0.0
        completed = [t for t in tasks if t.status == TaskStatus.COMPLETED]
        return round(len(completed) / len(tasks) * 100, 2)
