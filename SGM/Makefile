# Makefile
#!/bin/bash
# Poetry is a tool for dependency management and packaging in Python.
#It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

start: update
	poetry run python app.py

update:
	poetry update

install poetry:
	pip install poetry

clean:
	git clean -Xdf

.PHONY: start clean update install