# ML-K8s-App-HF-WnB

[DRAFT]

This project aims to create an end-to-end ML app as a functional MVP.  
The app itself uses Hugging Face and Weights&amp;Biases to reduce initial complexity. The ML modules used should be interchangeable without interrupting the pipeline. The app can be deployed into a Python venv, a Docker image and Kubernetes to showcase the separation of concerns of the different pipeline components. 

----> **Not fully implemented yet** <----

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

* [x] Basic exception handling
  * May be problematic with function returns
* [x] Type handling in function calls
  * Implemented to improve readability
  * May be extended with pydantic or python typing
* [x] Read multiple yml inside one file inside config loader
  * Abondoned, adds unnecessary complexity, use separate yml
* [x] Get sweep config
  * Implemented and functional
  * May be extended to other providers, but for MVP sufficient
* [x] Use `makefile` instead of `setup.sh`
  * Implemented and functional
  * Need improvement for local venv install, because `source` can not run inside `make`
* [x] Try `dataclass` and `field` from [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
  * Used to auto add special classes like `__init__`, `__str__`, `__repr__`
  * Uses type hinting and decorators
  * Abandoned, classes in this app not complex enough
* [x] Use [SemVer](https://semver.org/) for semantic versioning
  * Seems to be reasonable
* [ ] [Single source app version](https://packaging.python.org/guides/single-sourcing-package-version/)
* [ ] Use `if` for feature ensurance instead of `Ecxeption`
* [ ] Implement pydoc-action to auto-generate into gh-pages /docs
* [ ] Decouple concerns into separate containers
* [ ] Adhere to [Docker BP](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [ ] Adhere to BP from [The Hitchhiker’s Guide to Python!](https://docs.python-guide.org/)
* [ ] Implement basic CI/CD-Skeletton
* [ ] Have a look at [PyTest](http://pytest.org/)
* [ ] Test [pydantic](https://pydantic-docs.helpmanual.io/) for type checking and hinting
* [ ] Expand into [typing — Support for type hints](https://docs.python.org/3/library/typing.html)
* [ ] Try [`argparse`](https://docs.python.org/3/library/argparse.html)
* [ ] Implement basic API, e.g. with [gunicorn](https://github.com/benoitc/gunicorn) or [FastAPI](https://github.com/tiangolo/fastapi)
* [ ] Experiment with [`pyproject.toml`](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) to build app wheel