import pytest
from uuid import uuid4
from app.shared.utils.time import get_utc_now
from app.domain.models.todo_list import ToDoList
from app.domain.models.task import Task, TaskStatus, TaskPriority

@pytest.fixture
def sample_todo_list():
    return ToDoList(
        id=uuid4(),
        name="Sample List",
        description="Sample Description",
        created_at=get_utc_now(),
        updated_at=get_utc_now()
    )

@pytest.fixture
def sample_task(sample_todo_list):
    return Task(
        id=uuid4(),
        todo_list_id=sample_todo_list.id,
        title="Sample Task",
        description="Sample Description",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM,
        created_at=get_utc_now(),
        updated_at=get_utc_now()
    )
