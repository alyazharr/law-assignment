import os
import sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

from celery.result import AsyncResult
from fastapi import APIRouter
from starlette.responses import JSONResponse

from celery_tasks.tasks import get_all_task_recommendation_by_city, \
get_all_task_send_email, get_all_task_add_recommendation_to_bookmark, get_all_task_send_email_mybookmark

from config.celery_utils import get_task_info
from schemas.schemas import Email, BookmarkRecommend, BookmarkEmail

router = APIRouter(prefix='/recommendation', tags=['Weather'], responses={404: {"description": "Not found"}})

places_to_go = []

@router.get("/where-to-go/{provinsi}/{city}/{amount}")
async def places_recommendation(provinsi: str, city:str, amount:int) -> dict:
    task = get_all_task_recommendation_by_city.apply_async(args=(provinsi, city, amount))
    return JSONResponse({"task_id": task.id})

@router.post("/send-email")
async def send_email_recommendation(email: Email) -> dict:
    result_task = get_task_info(email.task_id)
    res = result_task['task_result']

    task_result = AsyncResult(email.task_id)
    if not task_result.ready():
        return JSONResponse({"error": "Task not yet complete"})

    # task has completed, send the email
    task = get_all_task_send_email.apply_async(args=(email.task_id, email.email_addr, res))
    return JSONResponse({"task_id": task.id})

#create
@router.post("/places-to-go/save")
async def add_recommendation_to_bookmark(recommend: BookmarkRecommend) -> dict:
    result_task = get_task_info(recommend.task_id)
    res = result_task['task_result']

    task_result = AsyncResult(recommend.task_id)
    if not task_result.ready():
        return JSONResponse({"error": "Task not yet complete"})
    
    task = get_all_task_add_recommendation_to_bookmark.apply_async(args=(recommend.task_id,res))
    return JSONResponse({"task_id": task.id})

#create
@router.post("/my-bookmark-places/save")
async def add_recommendation_to_bookmark(recommend: BookmarkRecommend) -> dict:
    result_task = get_task_info(recommend.task_id)
    res = result_task['task_result']

    task_result = AsyncResult(recommend.task_id)
    if not task_result.ready():
        return JSONResponse({"error": "Task not yet complete"})
    
    places_to_go.append(res)
    return {'message': f'New bookmark list of place by recommendation created successfully.'}

#read
@router.get("/my-bookmark-places")
def get_bookmark_place() -> dict:
    return {'results':places_to_go}

@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    return get_task_info(task_id)

@router.post("/get-my-bookmark/send-email")
async def send_email_mybookmark(email: BookmarkEmail) -> dict:
    # task has completed, send the email
    task = get_all_task_send_email_mybookmark.apply_async(args=(email.email_addr, places_to_go))
    return JSONResponse({"task_id": task.id})
