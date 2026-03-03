all:
	docker-compose up -d --build

down:
	docker-compose down -v
up:
	poetry run alembic revision --autogenerate
	poetry run upgrade head

run:
	poetry run uvicorn main:app --host 0.0.0.0 --port 12951 --reload
