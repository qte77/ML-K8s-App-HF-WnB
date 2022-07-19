HASH != git rev-parse --short HEAD
VENV_USED := $(HOME)/venvs/ML-venv

build:
	podman build --target baseimage \
		-t ml-baseimage:$(HASH) .
	podman build --target usecase \
		-t ml-usecase:$(HASH) .

local:
	echo Installing python and virtualenv
	/usr/bin/env python3 -m ensurepip
	/usr/bin/env python3 -m pip install --upgrade pip setuptools pipenv
	/usr/bin/env python3 -m pipenv install ./app
	echo Starting app
	/usr/bin/env python ./app/app.py
