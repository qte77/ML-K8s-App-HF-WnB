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
	/usr/bin/env python3 -m pip install --upgrade \
		pip setuptools virtualenv
	/usr/bin/env virtualenv -p python3 $(VENV_USED) # --no-site-packages
	#TODO use source inside makefile not possible
	#workaround: source inside sh inside makefile with EOF
	# source $(VENV_USED)/bin/activate
	# echo Installing requirements into venv
	# /usr/bin/env pip install -r ./app/requirements.txt
	# echo Starting app
	# /usr/bin/env python ./app/app.py
