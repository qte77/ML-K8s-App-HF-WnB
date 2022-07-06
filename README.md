# ML-K8s-App-HF-WnB

[DRAFT]

End-to-end  ML app as a MVP. The app itself uses Hugging Face and Weights&amp;Biases to reduce initial complexity. The ML modules used should be interchangeable without interrupting the pipeline. The app can be deployed into a local venv, a docker image and K8s to showcase the separation of concerns of the different layers. 

----> **Not fully implemented yet** <----

## TOC

* [Purpose](#purpose-)
* [App structure](#app-structure-)
* [Install](#install-)
* [TODO](#todo-)

## Purpose [↑](#ml-k8s-app-hf-wnb)

* Showcase an end-to-end app with train and inference mode
* Implement self-contained modular pipeline
* Models can be loaded from registries 

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

### Local python venv

`make local`

### Docker

`make build`

### Kubernetes

**TODO**

## TODO [↑](#ml-k8s-app-hf-wnb)

* Test-if instead of exception handling
* Get sweep config
* Arg parsing
* pydoc
* Python hitchhiker BP
* Makefile
* Decouple concerns into separate containers
* Adhere to [Docker BP](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* CI/CD-Skeletton
* Have a look at [PyTest](http://pytest.org/)
* Test [pydantic](https://pydantic-docs.helpmanual.io/) for type checking and hinting
* Expand into [typing — Support for type hints](https://docs.python.org/3/library/typing.html)
