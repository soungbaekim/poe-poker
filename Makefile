.PHONY: setup deploy

setup:
	pip3 install -r requirements.txt

deploy:
	modal deploy server/__init__.py

deploy-cat:
	modal deploy catbot/__init__.py

upload:
	modal volume put firebase firebase.json key.json