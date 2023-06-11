from fastapi import FastAPI

from src.admin.routers import admin_router

app = FastAPI()

app.include_router(admin_router)
