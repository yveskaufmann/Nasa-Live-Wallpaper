.PHONY: start

start:
	python -m nasa_wallpaper

setup:
	pipenv install
	pipenv shell