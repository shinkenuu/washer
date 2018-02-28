export DATABASE_URL=postgres://washer:washer@192.168.0.101:5432/washer
export FLASK_APP=./app/__init__.py
export FLASK_DEBUG=1

help: ## Show this help message.
	echo "runserver"
	echo "test"

runserver:
	flask run

db:
    flask db

test:
	pytest ./tests/
