from app.domain.repositories.todo_list_repository_interface import (
    ToDoListRepositoryInterface,
)
from app.domain.models.todo_list import ToDoListCreate, ToDoListUpdate, ToDoList
from app.shared.utils.time import get_utc_now
from app.infrastructure.db.models import ToDoListORM
from uuid import UUID
from typing import List
from sqlalchemy.orm import Session


class ToDoListRepository(ToDoListRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: ToDoListCreate) -> ToDoList:
        db_obj = ToDoListORM(**data.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return ToDoList(**db_obj.__dict__)

    def get_by_id(self, list_id: UUID) -> ToDoList:
        obj = self.db.query(ToDoListORM).filter(ToDoListORM.id == list_id).first()
        return ToDoList(**obj.__dict__) if obj else None

    def update(self, list_id: UUID, data: ToDoListUpdate) -> ToDoList:
        obj = self.db.query(ToDoListORM).filter(ToDoListORM.id == list_id).first()
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        obj.updated_at = get_utc_now()
        self.db.commit()
        self.db.refresh(obj)
        return ToDoList(**obj.__dict__)

    def delete(self, list_id: UUID) -> bool:
        obj = self.db.query(ToDoListORM).filter(ToDoListORM.id == list_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def list_all(self) -> List[ToDoList]:
        objs = self.db.query(ToDoListORM).all()
        return [ToDoList(**obj.__dict__) for obj in objs]
