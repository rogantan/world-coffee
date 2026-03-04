all:
	docker-compose up -d --build
downv:
	docker-compose down -v
down:
	docker-compose down
up:
	poetry run alembic revision --autogenerate
	poetry run alembic upgrade head
run:
	poetry run uvicorn main:app --host 0.0.0.0 --port 12951 --reload