# ML-K8s-App-HF-WnB

[DRAFT] [WIP] **----> Not fully implemented yet**

This project aims to create an end-to-end ML app as a functional MVP.  
The app itself uses Hugging Face (HF) and Weights&amp;Biases (WandB) to reduce initial complexity. The ML modules used should be interchangeable without interrupting the pipeline. The app can be deployed into a Python venv, a Docker image and Kubernetes to showcase the separation of concerns of the different pipeline components. 

## TOC

* [Purpose](#purpose-)
* [App structure](#app-structure-)
* [Install](#install-)
* [TODO](#todo-)

## Purpose [↑](#ml-k8s-app-hf-wnb)

* Showcase an end-to-end app with train and inference mode
* Implement self-contained modular pipeline

## App structure [↑](#ml-k8s-app-hf-wnb)

* Dockerfile
* makefile
* /app
  * app.py
  * requirements.txt
  * /config
  * /modules
* /kubernetes
  * /base
  * /overlay

## Install [↑](#ml-k8s-app-hf-wnb)

### Python venv

`make local`

### Docker

`make build`

### Kubernetes

**TODO**

## TODO [↑](#ml-k8s-app-hf-wnb)

### Coding

* [x] Get WandB sweep config
  * Implemented and functional
  * May be extended to other providers, but for MVP sufficient
* [x] Basic exception handling
  * May be problematic with function returns
* [x] Type handling in function calls
  * Implemented to improve readability
  * May be extended with pydantic or python typing
* [x] Read multiple yml inside one file inside config loader
  * Abondoned, adds unnecessary complexity, use separate yml
* [x] Try `dataclass` and `field` from [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
  * Used to auto add special classes like `__init__`, `__str__`, `__repr__`
  * Uses type hinting and decorators
  * Abandoned, classes in this app not complex enough
* [ ] Use `if` for to check if feature can be provided properly instead of `Ecxeption` to catch it
* [ ] Decouple concerns into separate containers, e.g. avoid big container because of `torch`
* [ ] Test [pydantic](https://pydantic-docs.helpmanual.io/) for type checking and hinting
* [ ] Expand into [typing — Support for type hints](https://docs.python.org/3/library/typing.html)
* [ ] Try [`argparse`](https://docs.python.org/3/library/argparse.html)
* [ ] Implement basic API, e.g. with [gunicorn](https://github.com/benoitc/gunicorn) or [FastAPI](https://github.com/tiangolo/fastapi)

### Dependency tracking and app sourcing

* [ ] Explore use of [pipenv with Pipfile & Pipfile.lock](https://pipenv.pypa.io/en/latest/basics/) as a [proposed replacement](https://github.com/pypa/pipfile#the-concept) to [requirements.txt]()
  * `pipenv install -e` for [editable mode](https://pipenv.pypa.io/en/latest/basics/#a-note-about-vcs-dependencies), i.e. 'dependency resolution can be performed with an up to date copy of the repository each time it is performed' 
* [ ] Experiment with [`pyproject.toml`](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) to build app wheel
* [ ] Provide package as [single source app version](https://packaging.python.org/guides/single-sourcing-package-version/) with `setup.py`

### Project management

* [x] Use `makefile` instead of self-implemented imparative `setup.sh`
  * Implemented and functional
  * Need improvement for local venv install, because `source` can not run inside `make`
* [x] Adopt [SemVer](https://semver.org/) for semantic versioning
  * Seems to be reasonable
* [ ] Implement basic CI/CD-Skeleton
* [ ] Have a look at [PyTest](http://pytest.org/)
* [ ] Implement pydoc-action to auto-generate into gh-pages /docs, e.g. [Sphinx Build Action](https://github.com/marketplace/actions/sphinx-build) for [Sphinx](https://www.sphinx-doc.org/en/master/usage/quickstart.html)

### Best practices

* [ ] Adhere to [Docker BP](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [ ] Adhere to BP from [The Hitchhiker’s Guide to Python!](https://docs.python-guide.org/)
