.PHONY: setup deploy

setup:
	pip3 install -r requirements.txt

deploy:
	modal deploy catbot/__init__.py
