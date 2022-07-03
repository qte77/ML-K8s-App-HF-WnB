docker: Dockerfile
    podman image build --tag ML-pipeline:latest

local: app.py
	echo 'Installing python and virtualenv "ML-venv"'
    /usr/bin/env/python -m ensurepip
    /usr/bin/env/pip install --upgrade pip setuptools virtualenv
    virtualenv -p python3 ML-venv --no-site-packages
    source ML-venv/bin/activate
    echo "Installing requirements into "ML-venv"'
    /usr/bin/env/pip install -r ./app/requirements.txt
    echo 'Starting app'
    /usr/bin/env/python ./app/app.py
