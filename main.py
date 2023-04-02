import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

import time
import uvicorn
from fastapi import FastAPI

from config.celery_utils import create_celery
from routers import weather, rekomendasi


def create_app() -> FastAPI:
    current_app = FastAPI(title="Asynchronous tasks processing with Celery and RabbitMQ",
                          description="Prediksi Cuaca Pada Tiap Provinsi",
                          version="1.0.0", )

    current_app.celery_app = create_celery()
    current_app.include_router(weather.router)
    current_app.include_router(rekomendasi.router)
    return current_app

app = create_app()
celery = app.celery_app

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
