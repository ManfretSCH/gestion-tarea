from fastapi import FastAPI
from app.database import engine, base
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router

base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(
    tasks_router,
    prefix="/users/{user_id}/tasks",
    tags=["tasks"]
)

app.include_router(
    users_router,
    prefix="/users",
    tags=["users"]
)