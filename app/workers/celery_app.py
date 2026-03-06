import os
from celery import Celery

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

celery_app = Celery(
    "amazonish",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.task_default_queue = "default"

celery_app.conf.task_routes = {
    "app.workers.tasks.*": {"queue": "default"},
}

celery_app.conf.timezone = "UTC"

celery_app.autodiscover_tasks(["app.workers"])
