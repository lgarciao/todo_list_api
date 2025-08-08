from app.domain.repositories.task_repository_interface import TaskRepositoryInterface
from app.domain.models.task import (
    TaskCreate,
    TaskUpdate,
    Task,
    TaskStatus,
    TaskPriority,
)
from app.infrastructure.db.models import TaskORM
from app.shared.utils.time import get_utc_now
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session


class TaskRepository(TaskRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create(self, list_id: UUID, data: TaskCreate) -> Task:
        db_obj = TaskORM(**data.model_dump(), todo_list_id=list_id)
        db_obj.created_at = get_utc_now()
        db_obj.updated_at = get_utc_now()
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return Task(**db_obj.__dict__)

    def get_by_id(self, list_id: UUID, task_id: UUID) -> Task:
        obj = (
            self.db.query(TaskORM)
            .filter(TaskORM.todo_list_id == list_id, TaskORM.id == task_id)
            .first()
        )
        return Task(**obj.__dict__) if obj else None

    def update(self, list_id: UUID, task_id: UUID, data: TaskUpdate) -> Task:
        obj = (
            self.db.query(TaskORM)
            .filter(TaskORM.todo_list_id == list_id, TaskORM.id == task_id)
            .first()
        )
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        obj.updated_at = get_utc_now()
        self.db.commit()
        self.db.refresh(obj)
        return Task(**obj.__dict__)

    def delete(self, list_id: UUID, task_id: UUID) -> bool:
        obj = (
            self.db.query(TaskORM)
            .filter(TaskORM.todo_list_id == list_id, TaskORM.id == task_id)
            .first()
        )
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def list_by_filters(
        self,
        list_id: UUID,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[Task]:
        query = self.db.query(TaskORM).filter(TaskORM.todo_list_id == list_id)
        if status:
            query = query.filter(TaskORM.status == status)
        if priority:
            query = query.filter(TaskORM.priority == priority)
        objs = query.all()
        return [Task(**obj.__dict__) for obj in objs]
