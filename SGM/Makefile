# Makefile
#!/bin/bash
# Poetry is a tool for dependency management and packaging in Python.
#It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

start: update
	poetry run python app.py # run project

update:
	poetry update # update poetry requirements

install poetry:
	pip install poetry # install poetry to your system

clean:
	git clean -Xdf # Delete all files in .gitignore

.PHONY: start clean update install