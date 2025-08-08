from fastapi import HTTPException, status


class ToDoListNotFoundException(HTTPException):
    def __init__(self, list_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ToDo List with ID '{list_id}' not found.",
        )


class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found.",
        )


class InvalidTaskStatusException(HTTPException):
    def __init__(self, status_value: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid task status: '{status_value}'.",
        )
