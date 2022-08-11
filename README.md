App-K8s-HF-WnB
===

[![CodeQL](https://github.com/qte77/App-K8s-HF-WnB/actions/workflows/codeql.yml/badge.svg)](https://github.com/qte77/App-K8s-HF-WnB/actions/workflows/codeql.yml)
[![Lint Code Base](https://github.com/qte77/App-K8s-HF-WnB/actions/workflows/linter.yml/badge.svg)](https://github.com/qte77/App-K8s-HF-WnB/actions/workflows/linter.yml)
[![Links (Fail Fast)](https://github.com/qte77/App-K8s-HF-WnB/actions/workflows/links-fail-fast.yml/badge.svg)](https://github.com/qte77/App-K8s-HF-WnB/actions/workflows/links-fail-fast.yml)
[![wakatime](https://wakatime.com/badge/github/qte77/App-K8s-HF-WnB.svg)](https://wakatime.com/badge/github/qte77/App-K8s-HF-WnB)

This project aims to create an end-to-end ML app as a functional MVP.
The app itself uses Hugging Face (HF) and Weights&amp;Biases (WandB) to reduce initial complexity. The ML modules used should be interchangeable without interrupting the pipeline. The app can be deployed into a Python venv, a Docker image and Kubernetes to showcase the separation of concerns of the different pipeline components.

Status
---

**[DRAFT]** **[WIP]** **----> Not fully implemented yet**

The current version is <1.8.0>. For version history have a look at [CHANGELOG.md](./CHANGELOG.md).

Quickstart
---

* TODO <!-- `make run_all` -->

TOC
---

* [Usage](#usage-)
* [Install](#install-)
* [Reason](#reason-)
* [Purpose](#purpose-)
* [Paradigms](#paradigms-)
* [App Structure](#app-structure-)
* [App Details](#app-details-)
* [TODO](#todo-)
* [Inspirations](#inspirations-)
* [Rescources](#resources-)

Usage [↑](#app-k8s-hf-wnb)
---

If inside the venv

```sh
python -m app
```

or if outside

```sh
pipenv run python -m app
```

Install [↑](#app-k8s-hf-wnb)
---

### Python

From an environment with available `make`

```sh
make setup_local_dev
```

or from an environment with available `pipenv`

```sh
python -m pipenv install --dev -e .
```

or with `conda`

```sh
$envname = 'TDD-Playground'
# create new conda venv with pipenv installed
conda create -ym -n $envname pipenv
conda activate $envname
# install from Pipfile and create new venv
python -m pipenv install --dev
# run command inside pipenv venv
python -m pipenv run python --version
python -m pipenv run pip list
```

or with `conda-forge`

```sh
conda install -c conda-forge pipfile
```

### Docker

* TODO <!-- `make build` -->

### Kubernetes

* TODO <!-- `make k8s-prod` or `make k8s-test` -->

Reason [↑](#app-k8s-hf-wnb)
---

* TODO

Purpose [↑](#app-k8s-hf-wnb)
---

* Showcase an end-to-end app with train and inference mode
* Implement self-contained modular pipeline

Paradigms [↑](#app-k8s-hf-wnb)
---

* TODO

App Structure [↑](#app-k8s-hf-wnb)
---

<details>
<summary>Show essential structure</summary>
<pre>
/
├─ app/
│  ├─ config/
│  ├─ helper/
│  ├─ model/
│  └─ app.py
├─ kubernetes/
│  ├─ base/
│  └─ overlay/
├─ CHANGELOG.md
├─ Dockerfile
├─ LICENSE
├─ Makefile
├─ Pipfile
├─ pyproject.toml
└─ README.md
</pre>
</details>

<details>
<summary>Show full structure</summary>
<pre>
/
├─ app/
│  ├─ config/
│  │  ├─ defaults.yml
│  │  ├─ huggingface.yml
│  │  ├─ logging.conf
│  │  ├─ sweep-wandb.yml
│  │  ├─ sweep.yml
│  │  ├─ task.yml
│  │  ├─ wandb.key.dummy.yml
│  │  └─ wandb.yml
│  ├─ helper/
│  │  ├─ config_logger.py
│  │  ├─ load_configs.py
│  │  ├─ load_hf_components.py
│  │  ├─ parametrise_pipeline.py
│  │  ├─ Pipeline.py
│  │  ├─ prepare_ml_input.py
│  │  └─ prepare_sweep.py
│  ├─ model/
│  │  ├─ inferModel.py
│  │  └─ trainModel.py
│  ├─ __main__.py
│  ├─ __version__.py
│  ├─ _version.py
│  ├─ app.py
│  └─ py.typed
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
├─ .bumpversion.cfg
├─ .flake8
├─ .gitignore
├─ .gitmessage
├─ .markdownlint.yml
├─ .pre-commit-config.yaml
├─ CHANGELOG.md
├─ Dockerfile
├─ LICENSE
├─ make.bat
├─ Makefile
├─ Pipfile
├─ Pipfile.lock
├─ pyproject.toml
└─ README.md
</pre>
</details>

TODO [↑](#app-k8s-hf-wnb)
---

### Coding

* [x] Get WandB sweep config
  * Implemented and functional
  * May be extended to other providers, but for MVP sufficient
* [x] Basic exception handling
  * May be problematic with function returns
* [x] Type hinting in function calls
  * Implemented to improve readability
  * May be extended with `typing`, `dataclasses` or `pydantic`
* [x] Read multiple yml inside one file inside config loader
  * Abondoned, adds unnecessary complexity, use separate yml
* [x] Try `dataclass` and `field` from [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
  * Used to auto add special classes like `__init__`, `__str__`, `__repr__`
  * Uses type hinting and decorators
  * Abandoned, classes in this app not complex enough
* [ ] Test [pydantic](https://pydantic-docs.helpmanual.io/) for type checking and hinting instead of `typing` or `dataclasses`
* [ ] Expand into [typing — Support for type hints](https://docs.python.org/3/library/typing.html)
* [ ] Use `if` for to check if feature can be provided properly instead of `Ecxeption` to catch it
* [ ] Decouple concerns into separate containers, e.g. avoid big container because of `torch`
  * Difference between Abstraction vs Decoupling
* [ ] Try [`argparse`](https://docs.python.org/3/library/argparse.html)
* [ ] Implement basic API, e.g. with [gunicorn](https://github.com/benoitc/gunicorn) or [FastAPI](https://github.com/tiangolo/fastapi)
* [ ] Use `hydra`and/or `omegaconf` to load configs instead of own helper implementation
* Factor out `Pipeline.py` into functional only
  * Sole purpose of `Pipeline.py` is to represent the gathered configs

### Dependency tracking and app sourcing

* [x] Explore use of [pipenv with Pipfile & Pipfile.lock](https://pipenv.pypa.io/en/latest/basics/) as a [proposed replacement](https://github.com/pypa/pipfile#the-concept) to `requirements.txt`
  * `pipenv install -e` for [editable mode](https://pipenv.pypa.io/en/latest/basics/#a-note-about-vcs-dependencies), i.e. 'dependency resolution can be performed with an up to date copy of the repository each time it is performed'
* [x] Experiment with [`pyproject.toml`](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) to build app wheel
  * Used to pool information for build, package, tools etc into one file
  * Some tools like `flake8` do not support this approach
* [ ] Provide package as [single source app version](https://packaging.python.org/guides/single-sourcing-package-version/) with `setup.py`
  * Required for `tox`

### Project management

* [x] Use `Makefile` instead of self-implemented imparative `setup.sh`
  * Implemented and functional
  * Need improvement for local venv install, because `source` can not run inside `make`
* [x] Adopt [CHANGELOG.md](https://keepachangelog.com/en/1.0.0/)
  * 'A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project.'
  * Seems to be reasonable
* [x] Adopt [SemVer](https://semver.org/) for semantic versioning
  * Seems to be reasonable
* [x] Implement basic CI/CD-Skeleton
  * Using `bump2version`, `pre-commit`, `black` etc
* [x] Have a look at [PyTest](http://pytest.org/)
  * Explored in repo `TDD-Playground`
* [ ] Implement pydoc-action to auto-generate into gh-pages /docs, e.g. [Sphinx Build Action](https://github.com/marketplace/actions/sphinx-build) for [Sphinx](https://www.sphinx-doc.org/en/master/usage/quickstart.html)

Inspirations [↑](#app-k8s-hf-wnb)
---

* TODO

Ressources [↑](#app-k8s-hf-wnb)
---

* TODO
