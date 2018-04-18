export DATABASE_URL=postgres://washer:washer@127.0.0.1:5432/washer

help:
	# test

test:
	pytest ./tests/
