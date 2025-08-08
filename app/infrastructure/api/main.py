from fastapi import FastAPI
from app.infrastructure.api.routers.todo_list_router import router as todo_list_router
from app.infrastructure.api.routers.task_router import router as task_router

app = FastAPI(title="To Do List API")

app.include_router(todo_list_router)
app.include_router(task_router)
