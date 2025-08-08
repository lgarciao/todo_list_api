import pytest
from uuid import UUID, uuid4
from datetime import datetime
from app.shared.utils.time import get_utc_now
from app.domain.models.task import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from app.domain.exceptions.custom_exceptions import TaskNotFoundException
from app.application.use_cases.task_use_case import TaskUseCase
from tests.unit_test.test_todo_list import MockToDoListRepository


class MockTaskRepository:
    def __init__(self):
        self.tasks = {}

    def create(self, todo_list_id: UUID, data: TaskCreate) -> Task:
        task_id = uuid4()
        now = get_utc_now()
        task = Task(
            id=task_id,
            todo_list_id=todo_list_id,
            title=data.title,
            description=data.description,
            status=data.status,
            priority=data.priority,
            created_at=now,
            updated_at=now
        )
        self.tasks[task_id] = task
        return task

    def get_by_id(self, todo_list_id: UUID, task_id: UUID, *args, **kwargs) -> Task:
        task = self.tasks.get(task_id)
        if not task or task.todo_list_id != todo_list_id:
            raise TaskNotFoundException(task_id)
        return task

    def update(self, todo_list_id: UUID, task_id: UUID, data: TaskUpdate, *args, **kwargs) -> Task:
        task = self.tasks.get(task_id)
        if not task or task.todo_list_id != todo_list_id:
            raise TaskNotFoundException(task_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        task.updated_at = get_utc_now()
        return task

    def delete(self, todo_list_id: UUID, task_id: UUID, *args, **kwargs) -> bool:
        task = self.tasks.get(task_id)
        if not task or task.todo_list_id != todo_list_id:
            raise TaskNotFoundException(task_id)
        del self.tasks[task_id]
        return True
    def list_by_filters(self, todo_list_id=None, status=None, priority=None, *args, **kwargs):
        # Simple filter for compatibility
        results = list(self.tasks.values())
        if todo_list_id is not None:
            results = [t for t in results if t.todo_list_id == todo_list_id]
        if status is not None:
            results = [t for t in results if t.status == status]
        if priority is not None:
            results = [t for t in results if t.priority == priority]
        return results

    def list_by_todo_list(self, todo_list_id: UUID) -> list[Task]:
        return [task for task in self.tasks.values() if task.todo_list_id == todo_list_id]


@pytest.fixture
def task_use_case():
    list_repository = MockToDoListRepository()
    task_repository = MockTaskRepository()
    use_case = TaskUseCase(todo_list_repository=list_repository, task_repository=task_repository)
    use_case.list_repository = list_repository  # Para acceso en los tests
    return use_case


def test_create_task(task_use_case):
    # Given
    todo_list_id = uuid4()
    from app.domain.models.todo_list import ToDoList
    now = get_utc_now()
    todo_list = ToDoList(id=todo_list_id, name="Test List", description="desc", created_at=now, updated_at=now)
    task_use_case.list_repository.add(todo_list)
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )

    # When
    created_task = task_use_case.create_task(todo_list_id, task_data)

    # Then
    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    assert created_task.status == TaskStatus.PENDING
    assert created_task.priority == TaskPriority.MEDIUM
    assert created_task.todo_list_id == todo_list_id
    assert isinstance(created_task.id, UUID)
    assert isinstance(created_task.created_at, datetime)
    assert isinstance(created_task.updated_at, datetime)


def test_get_task(task_use_case):
    # Given
    todo_list_id = uuid4()
    from app.domain.models.todo_list import ToDoList
    now = get_utc_now()
    todo_list = ToDoList(id=todo_list_id, name="Test List", description="desc", created_at=now, updated_at=now)
    task_use_case.list_repository.add(todo_list)
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    created_task = task_use_case.create_task(todo_list_id, task_data)

    # When
    retrieved_task = task_use_case.get_task(todo_list_id, created_task.id)

    # Then
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == created_task.title
    assert retrieved_task.description == created_task.description
    assert retrieved_task.status == created_task.status
    assert retrieved_task.priority == created_task.priority


def test_get_non_existent_task(task_use_case):
    # Given
    non_existent_task_id = uuid4()
    non_existent_list_id = uuid4()
    from app.domain.models.todo_list import ToDoList
    now = get_utc_now()
    todo_list = ToDoList(id=non_existent_list_id, name="Test List", description="desc", created_at=now, updated_at=now)
    # No agregamos la lista al mock, para simular que no existe

    # When/Then
    with pytest.raises(TaskNotFoundException):
        task_use_case.get_task(non_existent_list_id, non_existent_task_id)


def test_update_task(task_use_case):
    # Given
    todo_list_id = uuid4()
    from app.domain.models.todo_list import ToDoList
    now = get_utc_now()
    todo_list = ToDoList(id=todo_list_id, name="Test List", description="desc", created_at=now, updated_at=now)
    task_use_case.list_repository.add(todo_list)
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    created_task = task_use_case.create_task(todo_list_id, task_data)
    update_data = TaskUpdate(
        title="Updated Task",
        description="Updated Description",
        status=TaskStatus.COMPLETED,
        priority=TaskPriority.HIGH
    )

    # When
    updated_task = task_use_case.update_task(todo_list_id, created_task.id, update_data)

    # Then
    assert updated_task.id == created_task.id
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"
    assert updated_task.status == TaskStatus.COMPLETED
    assert updated_task.priority == TaskPriority.HIGH


def test_delete_task(task_use_case):
    # Given
    todo_list_id = uuid4()
    from app.domain.models.todo_list import ToDoList
    now = get_utc_now()
    todo_list = ToDoList(id=todo_list_id, name="Test List", description="desc", created_at=now, updated_at=now)
    task_use_case.list_repository.add(todo_list)
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM
    )
    created_task = task_use_case.create_task(todo_list_id, task_data)

    # When
    task_use_case.delete_task(todo_list_id, created_task.id)

    # Then
    with pytest.raises(TaskNotFoundException):
        task_use_case.get_task(todo_list_id, created_task.id)


def test_list_tasks_by_todo_list(task_use_case):
    # Given
    todo_list_id = uuid4()
    from app.domain.models.todo_list import ToDoList
    now = get_utc_now()
    todo_list = ToDoList(id=todo_list_id, name="Test List", description="desc", created_at=now, updated_at=now)
    task_use_case.list_repository.add(todo_list)
    task1 = task_use_case.create_task(todo_list_id, TaskCreate(
        title="Task 1",
        description="Description 1",
        status=TaskStatus.PENDING,
        priority=TaskPriority.LOW
    ))
    task2 = task_use_case.create_task(todo_list_id, TaskCreate(
        title="Task 2",
        description="Description 2",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH
    ))
    other_list_id = uuid4()
    other_list = ToDoList(id=other_list_id, name="Other List", description="desc", created_at=now, updated_at=now)
    task_use_case.list_repository.add(other_list)
    task_use_case.create_task(other_list_id, TaskCreate(
        title="Other Task",
        description="Other Description",
        status=TaskStatus.COMPLETED,
        priority=TaskPriority.MEDIUM
    ))

    # When
    list_tasks = task_use_case.list_tasks(todo_list_id)

    # Then
    assert len(list_tasks) == 2
    assert any(task.id == task1.id for task in list_tasks)
    assert any(task.id == task2.id for task in list_tasks)
