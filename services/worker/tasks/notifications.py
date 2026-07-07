from celery import Celery
import os

celery_app = Celery(
    "fitflow_worker",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)


@celery_app.task
def send_booking_confirmation(client_email: str, schedule_time: str):
    print(f"Отправка подтверждения на {client_email} для {schedule_time}")
    return {"status": "sent"}


@celery_app.task
def send_training_reminder(client_email: str, schedule_time: str):
    print(f"Отправка напоминания на {client_email} для {schedule_time}")
    return {"status": "sent"}