from celery import shared_task
from api import bmkg_weather
import uuid
from schemas.schemas import PlacesToGo
from email.message import EmailMessage
import ssl
import smtplib

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='bmkg_weather:get_today_weather_by_province')
def get_all_task_today_weather_by_province(self, provinsi:str):
    data = bmkg_weather.get_today_weather_by_province(provinsi=provinsi)
    return data

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='bmkg_weather:get_weather_forecast_by_province')
def get_all_task_weather_forecast_by_province(self, provinsi:str):
    data = bmkg_weather.get_weather_forecast_by_province(provinsi=provinsi)
    return data

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='bmkg_weather:get_today_weather_by_city')
def get_all_task_today_weather_by_city(self, provinsi:str, city:str):
    print("masuk sini nih bos")
    data = bmkg_weather.get_today_weather_by_city(provinsi=provinsi, city=city)
    print("data aman nih", data)
    return data

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='bmkg_weather:get_weather_forecast_by_city')
def get_all_task_weather_forecast_by_city(self, provinsi:str, city:str):
    data = bmkg_weather.get_weather_forecast_by_city(provinsi=provinsi, city=city)
    return data

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='bmkg_weather:recommendation_togo_by_city_weather')
def get_all_task_recommendation_by_city(self, *args):
    data = bmkg_weather.recommendation_togo_by_city_weather(*args)
    return data

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='bmkg_weather:send_email')
def get_all_task_send_email(self, task_id:str, email_addr:str, res:dict):
    print("this is task_id: ", task_id)
    print("this is email receiver: ", email_addr)
    print("this is res: ", res)

    SENDER_MAIL = "tugaslaw.2023@gmail.com"
    SENDER_MAIL_PASSWORD = "nidlfdqaogmttzjo"
    EMAIL_RECEIVER = email_addr

    subject = "Destination Recommendation - Request Number: "+task_id
    body = f"""
    Hi! My name is Azhar.
    I would like to send the recommendation that you request on number {task_id}.
    Here's the recommendation places you may go today to {res['nama']} on morning, afternoon, and evening.

    Where to go - Morning (06 AM up to 12 PM):
    {res['rekomendasi_pagi']}

    Where to go - Afternoon (12 PM up to 18 PM):
    {res['rekomendasi_siang']}
    

    Where to go - Evening (18 PM up to 00 AM):
    {res['rekomendasi_sore']}

    Enjoy the day!
    
    Regards,
    Azhar
    """
    em = EmailMessage()
    em['From'] = SENDER_MAIL
    em['To'] = EMAIL_RECEIVER
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    msg = ""
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(SENDER_MAIL, SENDER_MAIL_PASSWORD)
            smtp.sendmail(SENDER_MAIL, EMAIL_RECEIVER, em.as_string())
            msg = f"Email berhasil dikirimkan ke alamat email "+EMAIL_RECEIVER
    except Exception as e:
        msg = f"Gagal mengirim email: "+str(e)
    return {'message':msg}

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='bmkg_weather:add_recommendation_place_to_bookmark')
def get_all_task_add_recommendation_to_bookmark(self, task_id:str, res:dict):
    recom = {}
    recom['id'] = str(uuid.uuid4())

    rekom_pagi = []
    for place in res['rekomendasi_pagi']:
        new_book_place = PlacesToGo(
            index_id=str(uuid.uuid4()),
            place_id=place['id_tempat'],
            name=place['nama'],
            address=place['lokasi'],
            url=place['url_lokasi'],
            notes=''
        )
        rekom_pagi.append(new_book_place)

    rekom_siang = []
    for place in res['rekomendasi_siang']:
        new_book_place = PlacesToGo(
            index_id=str(uuid.uuid4()),
            place_id=place['id_tempat'],
            name=place['nama'],
            address=place['lokasi'],
            url=place['url_lokasi'],
            notes=''
        )
        rekom_siang.append(new_book_place)
        
    rekom_sore = []
    for place in res['rekomendasi_sore']:
        new_book_place = PlacesToGo(
            index_id=str(uuid.uuid4()),
            place_id=place['id_tempat'],
            name=place['nama'],
            address=place['lokasi'],
            url=place['url_lokasi'],
            notes=''
        )
        rekom_sore.append(new_book_place)

    recom['rekomendasi_pagi'] = rekom_pagi
    recom['rekomendasi_siang'] = rekom_siang
    recom['rekomendasi_sore'] = rekom_sore

    return recom

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='bmkg_weather:send_email_mybookmark')
def get_all_task_send_email_mybookmark(self, email_addr:str, places_to_go:list):
    SENDER_MAIL = "tugaslaw.2023@gmail.com"
    SENDER_MAIL_PASSWORD = "nidlfdqaogmttzjo"
    EMAIL_RECEIVER = email_addr

    subject = "My Dream Destination - Bookmark Places"
    body = f"""
    Hi! My name is Azhar.
    Ready to travel?
    Here, I attach your **DREAM DESTINATION**
    Hope you can go there, one day, or maybe tomorrow!:D
   
    My Bookmark Places - Wanna go There!

    {places_to_go}

    Enjoy the day!

    Regards,
    Azhar
    """
    em = EmailMessage()
    em['From'] = SENDER_MAIL
    em['To'] = EMAIL_RECEIVER
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    msg = ""
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(SENDER_MAIL, SENDER_MAIL_PASSWORD)
            smtp.sendmail(SENDER_MAIL, EMAIL_RECEIVER, em.as_string())
            msg = f"Email berhasil dikirimkan ke alamat email "+EMAIL_RECEIVER
    except Exception as e:
        msg = f"Gagal mengirim email: "+str(e)
    return {'message':msg}
