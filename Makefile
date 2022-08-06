HASH != git rev-parse --short HEAD
IMG_BASE := ml-baseimage:$(HASH)
IMG_USECASE := ml-usecase:$(HASH)
IMG_USECASE_LOCAL := localhost:5000/$(IMG_USECASE)
DOCKERFILE := ./Dockerfile
APP_PATH := ./app
APP_MAIN := $(APP_PATH)/app.py
APP_PIPFILE := $(APP_PATH)/Pipfile
KUBE := ./kubernetes/overlays
KUBE_PROD := $(KUBE)/prod
KUBE_TEST := $(KUBE)/test

# local_install_dev:
# pipenv run pre-commit install
# pipenv run mypy --install-types --non-interactive

# local_update_dev:
# pipenv run pre-commit autoupdate

# local_test:
# https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports

# local_commit:
#  --show-diff-on-failure

python: $(APP_PIPFILE)
	echo Installing Pipfile
	/usr/bin/env python3 -m ensurepip
	/usr/bin/env python3 -m pip install --upgrade pip setuptools pipenv
	/usr/bin/env python3 -m pipenv install $(APP_PATH)
	echo Starting app
	/usr/bin/env python $(APP_MAIN)

build: $(DOCKERFILE)
	podman build --target baseimage -t $(IMG_BASE) .
	podman build --target usecase -t $(IMG_USECASE) .

get-reg:
	podman container run -dt -p 5000:5000 --name registry \
		--volume registry:/var/lib/registry:Z docker.io/library/registry:2

serve:
	build
	get-reg
	podman image tag $(IMG_USECASE) $(IMG_USECASE_LOCAL)
	podman image push $(IMG_USECASE_LOCAL) --tls-verify=false
	#podman image search localhost:5000/ --tls-verify=false
	#podman image rm $(IMG_USECASE) $(IMG_USECASE_LOCAL)

k8s-prod: $(KUBE_PROD)
	serve
	kubectl apply -k $(KUBE_PROD)

k8s-test: $(KUBE_TEST)
	podman-serve
	kubectl apply -k $(KUBE_TEST)

.PHONY: help

help: README.md
	@$(cat $^)

%: README.md
	help
