init:
	alembic init -t async migrations

makemigrations:
	alembic revision  --autogenerate -m 'initial commit'

up:
	alembic upgrade heads

down:
	alembic downgrade

current-mig:
	alembic current

flake8:
	flake8 .

docker_build:
	 docker build -t crun-python-runner -f checker/Dockerfile.runner .
