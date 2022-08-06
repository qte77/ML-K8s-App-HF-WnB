#!/usr/bin/env python
"""Parametrise and return a parameter object"""
# TODO rename 'defaults' more specific and descriptive
# TODO generalize provider parametrisation
# TODO refactor Pipeline-object out into function only?

from os import environ

from torch import device
from torch.cuda import is_available

from .load_configs import get_config

# from logging import debug, error, getLogger, root


def get_param_dict() -> dict:
    """
    Returns parameter dict with values filled with `helper.load_configs.get_config(<config>)`
    """
    defaults: dict = get_config("defaults")
    hf_params: dict = get_config("huggingface")
    sweep: dict = get_config("sweep")
    task: dict = get_config("task")

    paramobj = {}
    paramobj["sweep"] = get_sweep_cfg(sweep)
    paramobj["device"] = _get_device()
    paramobj["dataset"] = _get_dataset_cfg(hf_params["datasets"], task["dataset"])
    paramobj["project_name"] = _get_project_name(
        task["model"],
        paramobj["dataset"]["name"],
        paramobj["device"],
        paramobj["sweep"]["is_sweep"],
    )
    if paramobj["sweep"]["is_sweep"]:
        # TODO case
        if paramobj["sweep"]["provider"] == "wandb":
            wandb_params = get_config("wandb")
            paramobj["wandb"] = _get_wandb_env(wandb_params, paramobj["project_name"])
    paramobj["defaults"] = _get_defaults(defaults)
    paramobj["model_full_name"] = _get_model_full_name(
        hf_params["models"], task["model"]
    )
    paramobj["metrics"]["metric_to_optimize"] = _get_metric_to_optimize_cfg(
        hf_params["metrics_to_optimize"], task["metric_to_optimize"]
    )
    paramobj["metrics"]["metrics_to_load"] = _get_metrics_to_load(
        hf_params["metrics_secondary_possible"], task["metrics_to_load"]
    )

    return paramobj


def _get_defaults(defaults: dict) -> dict:
    """Returns the default values"""

    # if not defaults.save_dir == '':
    #   return { 'save_dir' : defaults.save_dir }
    # else:
    #   #TODO check whether dir exists
    #   return { 'save_dir' : './data' }

    return NotImplementedError


def _get_dataset_cfg(datasets: dict, dataset: str) -> dict:

    datasetobj = {}
    try:
        dataset = dataset.lower()
        (
            datasetobj["name"],
            datasetobj["configuration"],
            datasetobj["avg"],
            datasetobj["colsrename"],
            datasetobj["colstokens"],
            datasetobj["colsremove"],
        ) = datasets.get(dataset, ["Invalid dataset", ""])
        return datasetobj
    except Exception as e:
        return e


def _get_model_full_name(models: dict, model: str) -> str:

    try:
        model = model.lower()
        return models.get(model, ["Invalid model", ""])
    except Exception as e:
        return e


def _get_metric_to_optimize_cfg(
    metrics_to_optimize: dict, metric_to_optimize: str
) -> dict:

    metricsobj = {}
    try:
        metric_to_optimize = metric_to_optimize.lower()
        metricsobj["goal"], metricsobj["greater_is_better"] = metrics_to_optimize.get(
            metric_to_optimize, ["Invalid metric", ""]
        )
        return metricsobj
    except Exception as e:
        return e


def _get_metrics_to_load(
    metrics_to_load: list, metrics_secondary_possible: bool
) -> list:

    metrics = []
    try:
        for metric in metrics_to_load:
            metrics.append() if metrics_secondary_possible.count(metric) else print(
                f"{metric} not contained"
            )
        return metrics
    except Exception as e:
        return e


def _get_device() -> str:

    try:
        environ["TPU_NAME"]
        return "tpu"
    except:
        try:
            return device("cuda" if is_available() else "cpu")
        except Exception as e:
            return e


def _get_project_name(
    model: str, dataset_name: str, device: str, is_sweep: bool
) -> str:

    suffix = "-sweep" if is_sweep else ""
    try:
        return f"{model}-{dataset_name}-{device}{suffix}"
    except Exception as e:
        return e


def _get_wandb_env(wandb_params: object, project_name: str) -> dict:
    """
    Checks for API-key first. Returns exception if not found
    Expects keyfile as yaml:
      username: ''
      key: ''
    """
    try:
        wandb_user_key = get_config(wandb_params["wandb_keyfile"])
    except FileNotFoundError:
        return "API-key not found"
    except Exception as e:
        return e

    wandbobj = {}
    wandbobj["username"] = wandb_user_key["username"]
    wandbobj["key"] = wandb_user_key["key"]
    wandbobj["entity"] = wandb_params["entity"]
    wandbobj["project"] = project_name
    wandbobj["watch"] = wandb_params["watch"]
    wandbobj["save_code"] = wandb_params["save_code"]
    wandbobj["log_model"] = wandb_params["log_model"]

    return wandbobj


def get_sweep_cfg(sweep: object) -> dict:

    sweepobj = {}
    sweepobj["is_sweep"] = True if sweep.train_count > 1 else False
    if sweepobj["is_sweep"]:
        sweepobj["train_count"] = sweep.train_count
        sweepobj["provider"] = sweep.provider
        sweepobj["config"] = get_config(f"sweep-{sweep.provider}")

    return sweepobj
