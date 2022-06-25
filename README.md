# ML-K8s-App-HF-WnB

End-to-end K8s app with Hugging Face and Weights&amp;Biases.

[DRAFT] of a pipeline using Hugging Face and Weights&Biases.

----> **Not fully implemented yet** <----

## TOC

* [Purpose](./README.md#purpose-)
* [App](./README.md#app-)
* [Pipeline](./README.md#pipeline-)
* [Install](./README.md#install-)
* [TODO](./README.md#todo-)

## Purpose [↑](./README.md#ml-k8s-app-hf-wnb-)

* Showcase an end-to-end app with train and inference mode
* Implement self-contained modular pipeline
* Models can be loaded from registries 

## Repo structure [↑](./README.md#ml-pipeline-)

* `k8s-app` Components of a K8s pipeline, intended as a PoC for production

## App structure [↑](./README.md#ml-pipeline-)

## Install [↑](./README.md#ml-pipeline-)

### Kubernets

### Docker image

`podman image build --tag <tag>`  
e.g.  
`podman image build --tag ML-pipeline:latest`

#### Local python

`source ./setup-local.sh`

## TODO [↑](./README.md#ml-pipeline-)

* Exception handling
* Type handling in function calls
* Read multiple yml inside one file inside cfgloader
* Get sweep config
* Arg parsing
