# from celery import Celery

# celery_app = Celery(
#     "amazonish",
#     broker="redis://localhost:6379/0",
#     backend="redis://localhost:6379/0",
# )

# celery_app.conf.task_routes = {
#     "app.workers.tasks.*": {"queue": "default"},
# }


from celery import Celery

celery_app = Celery(
    "amazonish",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.task_default_queue = "default"

celery_app.conf.task_routes = {
    "app.workers.tasks.*": {"queue": "default"},
}

celery_app.conf.timezone = "UTC"

celery_app.autodiscover_tasks(["app.workers"])
