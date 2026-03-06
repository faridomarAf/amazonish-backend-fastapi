# Makefile
run:
	uvicorn app.main:app --reload

worker:
	celery -A app.workers.celery_app.celery_app worker --loglevel=info

migrate:
	alembic upgrade head

seed:
	python scripts/seed.py

test:
	pytest -v