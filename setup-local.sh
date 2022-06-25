#!/usr/bin/env sh
app_path="./app"
app="${app_path}/app.py"
pyreqs="${app_path}/config/requirements.txt"
venv="venv-mlpipeline"

if [ -f $pyreqs ]; then
    echo "Installing python and virtualenv $pipenv"
    python -m ensurepip
    pip install --upgrade pip setuptools virtualenv
    virtualenv -p python3 $venv --no-site-packages
    source $venv/bin/activate
    echo "Installing from $pyreqs into $venv"
    pip install -r $pyreqs
    echo "Starting $app"
    python $app
else
    echo "$pyreqs not found. Aborting." 
fi
