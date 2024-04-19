PYTHON = python3.10.12

runserver:
	python3 manage.py runserver

create:
	virtualenv -p ${PYTHON} venv/

migrate:
	poetry run python3 manage.py migrate

migrations:
	poetry run python3 manage.py makemigrations

superuser:
	poetry run python3 manage.py createsuperuser
