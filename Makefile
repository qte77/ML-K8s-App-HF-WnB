HASH != git rev-parse --short HEAD
DOCKERFILE := ./Dockerfile
APP_PATH := ./app
APP_MAIN := ${APP_PATH}/app.py
APP_PIPFILE := ${APP_PATH}/Pipfile
KUBE := ./kubernetes/overlays
KUBE_PROD := ${KUBE}/prod
KUBE_TEST := ${KUBE}/test

build: ${DOCKERFILE}
	podman build --target baseimage \
		-t ml-baseimage:$(HASH) .
	podman build --target usecase \
		-t ml-usecase:$(HASH) .

local: ${APP_PIPFILE}
	echo Installing Pipfile
	/usr/bin/env python3 -m ensurepip
	/usr/bin/env python3 -m pip install --upgrade pip setuptools pipenv
	/usr/bin/env python3 -m pipenv install ${APP_PATH}
	echo Starting app
	/usr/bin/env python ${APP_MAIN}

k8s-prod: ${KUBE_PROD}
	build
	kubectl apply -k ${KUBE_PROD}

k8s-test: ${KUBE_TEST}
	build
	kubectl apply -k ${KUBE_TEST}