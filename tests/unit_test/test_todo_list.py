import pytest
from uuid import UUID, uuid4
from datetime import datetime
from app.shared.utils.time import get_utc_now
from app.domain.models.todo_list import ToDoList, ToDoListCreate, ToDoListUpdate
from app.domain.exceptions.custom_exceptions import ToDoListNotFoundException
from app.application.use_cases.todo_list_use_case import ToDoListUseCase


class MockToDoListRepository:
    def __init__(self):
        self.lists = {}

    def create(self, data: ToDoListCreate) -> ToDoList:
        list_id = uuid4()
        now = get_utc_now()
        todo_list = ToDoList(
            id=list_id,
            name=data.name,
            description=data.description,
            created_at=now,
            updated_at=now
        )
        self.lists[list_id] = todo_list
        return todo_list

    def add(self, todo_list):
        self.lists[todo_list.id] = todo_list

    def get_by_id(self, list_id: UUID, *args, **kwargs) -> ToDoList:
        return self.lists.get(list_id)

    def update(self, list_id: UUID, data: ToDoListUpdate) -> ToDoList:
        if list_id not in self.lists:
            return None
        todo_list = self.lists[list_id]
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo_list, key, value)
        todo_list.updated_at = get_utc_now()
        return todo_list

    def delete(self, list_id: UUID) -> bool:
        if list_id not in self.lists:
            return False
        del self.lists[list_id]
        return True

    def list_all(self) -> list[ToDoList]:
        return list(self.lists.values())


@pytest.fixture
def todo_list_use_case():
    repository = MockToDoListRepository()
    return ToDoListUseCase(repository)


def test_create_todo_list(todo_list_use_case):
    # Given
    todo_list_data = ToDoListCreate(
        name="Test List",
        description="Test Description"
    )

    # When
    created_list = todo_list_use_case.create_list(todo_list_data)

    # Then
    assert created_list.name == "Test List"
    assert created_list.description == "Test Description"
    assert isinstance(created_list.id, UUID)
    assert isinstance(created_list.created_at, datetime)
    assert isinstance(created_list.updated_at, datetime)


def test_get_todo_list(todo_list_use_case):
    # Given
    todo_list_data = ToDoListCreate(
        name="Test List",
        description="Test Description"
    )
    created_list = todo_list_use_case.create_list(todo_list_data)

    # When
    retrieved_list = todo_list_use_case.get_list(created_list.id)

    # Then
    assert retrieved_list.id == created_list.id
    assert retrieved_list.name == created_list.name
    assert retrieved_list.description == created_list.description


def test_get_non_existent_list(todo_list_use_case):
    # Given
    non_existent_id = uuid4()

    # When/Then
    with pytest.raises(ToDoListNotFoundException):
        todo_list_use_case.get_list(non_existent_id)


def test_update_todo_list(todo_list_use_case):
    # Given
    todo_list_data = ToDoListCreate(
        name="Test List",
        description="Test Description"
    )
    created_list = todo_list_use_case.create_list(todo_list_data)
    update_data = ToDoListUpdate(
        name="Updated List",
        description="Updated Description"
    )

    # When
    updated_list = todo_list_use_case.update_list(created_list.id, update_data)

    # Then
    assert updated_list.id == created_list.id
    assert updated_list.name == "Updated List"
    assert updated_list.description == "Updated Description"


def test_delete_todo_list(todo_list_use_case):
    # Given
    todo_list_data = ToDoListCreate(
        name="Test List",
        description="Test Description"
    )
    created_list = todo_list_use_case.create_list(todo_list_data)

    # When
    todo_list_use_case.delete_list(created_list.id)

    # Then
    with pytest.raises(ToDoListNotFoundException):
        todo_list_use_case.get_list(created_list.id)


def test_list_all_todo_lists(todo_list_use_case):
    # Given
    list1 = todo_list_use_case.create_list(ToDoListCreate(
        name="List 1",
        description="Description 1"
    ))
    list2 = todo_list_use_case.create_list(ToDoListCreate(
        name="List 2",
        description="Description 2"
    ))

    # When
    all_lists = todo_list_use_case.list_all()

    # Then
    assert len(all_lists) == 2
    assert any(lst.id == list1.id for lst in all_lists)
    assert any(lst.id == list2.id for lst in all_lists)
