import os
import sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

from fastapi import APIRouter
from starlette.responses import JSONResponse

from celery_tasks.tasks import get_all_task_today_weather_by_city, get_all_task_today_weather_by_province, \
get_all_task_weather_forecast_by_city, get_all_task_weather_forecast_by_province

from config.celery_utils import get_task_info

router = APIRouter(prefix='/weather', tags=['Weather'], responses={404: {"description": "Not found"}})
@router.get("/today/{provinsi}")
async def get_today_cuaca_provinsi(provinsi: str) -> dict:
    task = get_all_task_today_weather_by_province.apply_async(args=(provinsi,))
    return JSONResponse({"task_id": task.id})

@router.get("/forecast/{provinsi}")
async def get_forecast_cuaca_provinsi(provinsi: str) -> dict:
    task = get_all_task_weather_forecast_by_province.apply_async(args=(provinsi,))
    return JSONResponse({"task_id": task.id})

@router.get("/today/{provinsi}/{city}")
async def get_today_cuaca_kota(provinsi: str, city:str) -> dict:
    task = get_all_task_today_weather_by_city.apply_async(args=(provinsi,city))
    return JSONResponse({"task_id": task.id})

@router.get("/forecast/{provinsi}/{city}")
async def get_forecast_cuaca_kota(provinsi: str, city:str) -> dict:
    task = get_all_task_weather_forecast_by_city.apply_async(args=(provinsi, city))
    return JSONResponse({"task_id": task.id})

@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    return get_task_info(task_id)