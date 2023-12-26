test:
	python -m unittest discover -s tests

build:
	docker build . -t dfreilich/backporter

clean:
	rm patch* result.* data/patch_* data/result.*

lint:
	python -m black . && python -m flake8 . --exclude venv