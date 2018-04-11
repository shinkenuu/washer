export DATABASE_URL=postgres://washer:washer@127.0.0.1:5432/test_washer
export FLASK_APP=./app/__init__.py
export FLASK_DEBUG=1

help:
	# runserver
	# db-upgrade
	# test

runserver:
	flask run

db-upgrade:
	flask db upgrade

test:
	pytest ./tests/
