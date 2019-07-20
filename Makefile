all: build

build:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*

.PHONY: build upload
