all: build

build:
	python3 setup.py sdist bdist_wheel

clean:
	rm -f dist/*

upload:
	twine upload dist/*

.PHONY: build upload
