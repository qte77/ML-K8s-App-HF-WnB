# ML-K8s-App-HF-WnB

End-to-end K8s app with Hugging Face and Weights&amp;Biases.

[DRAFT] of a pipeline using Hugging Face and Weights&Biases.

----> **Not fully implemented yet** <----

## TOC

* [Purpose](#purpose-)
* [Repo structure ](#repo-structure-)
* [App structure](#app-structure-)
* [Install](#install-)
* [TODO](#todo-)

## Purpose [↑](#ml-k8s-app-hf-wnb)

* Showcase an end-to-end app with train and inference mode
* Implement self-contained modular pipeline
* Models can be loaded from registries 

## Repo structure [↑](#ml-k8s-app-hf-wnb)

* `k8s-app` Components of a K8s pipeline, intended as a PoC for production

## App structure [↑](#ml-k8s-app-hf-wnb)

* Dockerfile
* makefile
* /app
 * app.py
 * requirements.txt
 * /config
 * /modules

### Modules

* train.py
* infer.py
* prepare.py
 * parametrise.py
  * loadcfg.py

## Install [↑](#ml-k8s-app-hf-wnb)

### Kubernetes

**TODO**

### Docker image

`podman image build --tag <tag>`  
e.g.  
`podman image build --tag ML-pipeline:latest`

#### Local python venv

`make makefile local`

## TODO [↑](#ml-k8s-app-hf-wnb)

* Test-if instead of exception handling
* Get sweep config
* Arg parsing
* pydoc
* Python hitchhiker BP
* Makefile
* Decouple concerns into separate containers
* Adhere to [Docker BP](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
