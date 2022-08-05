App-K8s-HF-WnB
===

This project aims to create an end-to-end ML app as a functional MVP.  
The app itself uses Hugging Face (HF) and Weights&amp;Biases (WandB) to reduce initial complexity. The ML modules used should be interchangeable without interrupting the pipeline. The app can be deployed into a Python venv, a Docker image and Kubernetes to showcase the separation of concerns of the different pipeline components.

Status
---

**[DRAFT]** **[WIP]** **----> Not fully implemented yet**

The current version is <1.0.0>. For version history have a look at [CHANGELOG.md](./CHANGELOG.md).

Quickstart
---

* Quickstart

TOC
---

<!--
* [Usage](#usage-)
* [Install](#install-)
-->
* [Purpose](#purpose-)
<!--
* [Reason](#reason-)
* [Paradigms](#paradigms-)
-->
* [App Structure](#app-structure-)
* [App Details](#app-details-)
* [TODO](#todo-)
* [Inspirations](#inspirations-)
* [Rescources](#resources-)

Purpose [↑](#app-k8s-hf-wnb)
---

* Showcase an end-to-end app with train and inference mode
* Implement self-contained modular pipeline

Install [↑](#app-k8s-hf-wnb)
---

### Local

`make local`

### Docker

`make build`

### Kubernetes

`make k8s-prod` or `make k8s-test`

App Structure [↑](#app-k8s-hf-wnb)
---

```sh
/
├─ app/
│  ├─ config/
│  │  ├─ defaults.yml
│  │  ├─ huggingface.yml
│  │  ├─ sweep.yml
│  │  ├─ sweep-wandb.yml
│  │  ├─ task.yml
│  │  ├─ wandb.key.dummy.yml
│  │  └─ wandb.yml
│  ├─ modules/
│  │  ├─ createPipelineObject.py
│  │  ├─ inferModel.py
│  │  ├─ loadConfigs.py
│  │  ├─ parametrisePipeline.py
│  │  ├─ prepareLoggingSweep.py
│  │  ├─ prepareMLInput.py
│  │  └─ trainModel.py
│  ├─ _version.py
│  ├─ app.py
│  └─ Pipfile
├─ kubernetes/
│  ├─ base/
│  │  ├─ deployment.yml
│  │  ├─ kustomization.yml
│  │  ├─ pvc.yml
│  │  └─ service.yml
│  └─ overlay/
│     ├─ prod/
│     │  ├─ ingress.yml
│     │  ├─ kustomization.yml
│     │  └─ namespace.yml
│     └─ test/
│        ├─ ingress.yml
│        ├─ kustomization.yml
│        └─ namespace.yml
├─ .gitignore
├─ .python-version
├─ CHANGELOG.md
├─ Dockerfile
├─ LICENSE
├─ Makefile
└─ README.md
```

TODO [↑](#app-k8s-hf-wnb)
---

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

* [x] Explore use of [pipenv with Pipfile & Pipfile.lock](https://pipenv.pypa.io/en/latest/basics/) as a [proposed replacement](https://github.com/pypa/pipfile#the-concept) to `requirements.txt`
  * `pipenv install -e` for [editable mode](https://pipenv.pypa.io/en/latest/basics/#a-note-about-vcs-dependencies), i.e. 'dependency resolution can be performed with an up to date copy of the repository each time it is performed'
* [ ] Experiment with [`pyproject.toml`](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) to build app wheel
* [ ] Provide package as [single source app version](https://packaging.python.org/guides/single-sourcing-package-version/) with `setup.py`

### Project management

* [x] Use `Makefile` instead of self-implemented imparative `setup.sh`
  * Implemented and functional
  * Need improvement for local venv install, because `source` can not run inside `make`
* [x] Adopt [CHANGELOG.md](https://keepachangelog.com/en/1.0.0/)
  * 'A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project.'
  * Seems to be reasonable
* [x] Adopt [SemVer](https://semver.org/) for semantic versioning
  * Seems to be reasonable
* [ ] Implement basic CI/CD-Skeleton
* [ ] Have a look at [PyTest](http://pytest.org/)
* [ ] Implement pydoc-action to auto-generate into gh-pages /docs, e.g. [Sphinx Build Action](https://github.com/marketplace/actions/sphinx-build) for [Sphinx](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
