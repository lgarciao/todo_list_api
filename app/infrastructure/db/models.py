from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.infrastructure.db.base import Base
from app.domain.models.task import TaskStatus, TaskPriority
from app.shared.utils.time import get_utc_now


class ToDoListORM(Base):
    __tablename__ = "todo_lists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    tasks = relationship(
        "TaskORM", back_populates="todo_list", cascade="all, delete-orphan"
    )


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    todo_list_id = Column(
        UUID(as_uuid=True), ForeignKey("todo_lists.id"), nullable=False
    )
    todo_list = relationship("ToDoListORM", back_populates="tasks")
