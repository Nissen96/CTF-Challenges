from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .init_db import init_db
from .api import api_router


init_db()

app = FastAPI()

# Serve backend
app.include_router(api_router, prefix="/api", )

# Serve frontend
app.mount("/", StaticFiles(directory="app/dist", html=True), name="frontend")
