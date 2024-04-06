.PHONY: setup deploy

setup:
	pip3 install -r requirements.txt

deploy:
	modal deploy server/__init__.py

deploy-cat:
	modal deploy catbot/__init__.py

upload:
	modal volume put firebase firebase.json key.json

update:
	curl -X POST https://api.poe.com/bot/fetch_settings/PlayPoker/TD3VyE38CaEd2BeUz5n2WY8JP4foffi2