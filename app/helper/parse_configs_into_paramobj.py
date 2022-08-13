#!/usr/bin/env python
"""Parse configs and return a parameter object"""
# TODO rename 'defaults' more specific and descriptive
# TODO generalize provider parametrisation
# TODO refactor Pipeline-object out into function only?

# from logging import debug
from os import environ
from typing import Union

from torch import device
from torch.cuda import is_available

from .load_configs import (  # get_default_save_dir,
    get_config_content,
    get_keyfile_content,
)

# from logging import debug, error, getLogger, root


def get_param_dict() -> dict:
    """
    Returns parameter dict with values filled with
    `helper.load_configs.get_config_content(<config>)`
    """

    hf_params: dict = get_config_content("huggingface")
    sweep: dict = get_config_content("sweep")
    task: dict = get_config_content("task")

    # save_dir = get_default_save_dir()

    paramobj = {}
    paramobj["metrics"] = {}
    # paramobj["savedir"] =
    paramobj["sweep"]: dict = _get_sweep_cfg(sweep)
    paramobj["device"]: str = str(_get_device())
    paramobj["dataset"]: dict = _get_dataset_cfg(hf_params["datasets"], task["dataset"])
    paramobj["project_name"]: str = _get_project_name(
        task["model"],
        paramobj["dataset"]["dataset"],
        paramobj["device"],
        paramobj["sweep"]["is_sweep"],
    )
    paramobj["model_full_name"]: str = _get_model_full_name(
        hf_params["models"], task["model"]
    )
    paramobj["metrics"]["metric_to_optimize"]: dict = _get_metric_to_optimize_cfg(
        hf_params["metrics_to_optimize"], task["metric_to_optimize"]
    )
    paramobj["metrics"]["metrics_to_load"] = _get_metrics_to_load(
        task["metrics_to_load"], hf_params["metrics_secondary_possible"]
    )

    if paramobj["sweep"]["is_sweep"]:
        if paramobj["sweep"]["provider"] == "wandb":
            wandb_params = get_config_content("wandb")
            paramobj["wandb"] = _get_wandb_env_params(
                wandb_params, paramobj["project_name"]
            )

    return paramobj


def _get_dataset_cfg(datasets: dict, dataset: str) -> dict:
    """Gets the configuration of the dataset"""

    try:
        return datasets[dataset.lower()]
    except Exception as e:
        return e


def _get_model_full_name(models: dict, model: str) -> str:
    """Loads the full name of the model"""

    try:
        return models.get(model.lower(), ["Invalid model", ""])
    except Exception as e:
        return e


def _get_metric_to_optimize_cfg(
    metrics_to_optimize: dict, metric_to_optimize: str
) -> dict:
    """Loads the primary metric to optimise for and its parameters"""

    metricsobj = {}
    try:
        # TODO {}.get(metric_to_optimize, ["Invalid metric", ""])
        metric_to_optimize = metric_to_optimize.lower()
        metricsobj["name"] = metric_to_optimize
        metricsobj["goal"] = metrics_to_optimize[metric_to_optimize]["goal"]
        metricsobj["greater_is_better"] = metrics_to_optimize[metric_to_optimize][
            "greater_is_better"
        ]
        return metricsobj
    except Exception as e:
        return e


def _get_metrics_to_load(
    metrics_to_load: list[str], metrics_secondary_possible: list[str]
) -> list:
    """Loads secondary metrices"""

    try:
        return [met for met in metrics_to_load if met in metrics_secondary_possible]
    except Exception as e:
        return e


def _get_device() -> str:
    """Returns the device as 'cpu', 'gpu' or 'tpu'"""

    # TODO make it platform independent, TPU_NAME used by Google Colab
    if "TPU_NAME" in environ:
        return "tpu"
    else:
        try:
            return device("cuda" if is_available() else "cpu")
        except Exception as e:
            return e


def _get_project_name(
    model: str, dataset_name: str, device: str, is_sweep: bool
) -> Union[str, Exception]:
    """Returns the project name as f'{model}-{dataset_name}-{device}{suffix}'"""

    suffix = "-sweep" if is_sweep else ""
    try:
        return f"{model}-{dataset_name}-{device}{suffix}"
    except Exception as e:
        return e


def _get_sweep_cfg(sweep: dict) -> dict:
    """Gets the configuration of the sweep"""

    sweepobj = {}
    sweepobj["is_sweep"] = True if int(sweep["train_count"]) > 1 else False

    if sweepobj["is_sweep"]:
        sweep_provider = sweep["provider"]
        sweepobj["provider"] = sweep_provider
        sweepobj["config"] = get_config_content(f"sweep-{sweep_provider}")
        sweepobj["train_count"] = sweep["train_count"]

    return sweepobj


def _get_wandb_env_params(wandb_params: object, project_name: str) -> dict:
    """
    Not Implemented yet: WANDB_NOTES, WANDB_TAGS
    Checks for API-key first. Returns exception if not found
    Expects keyfile as yaml:
      username: ''
      key: ''
    """

    wandbobj = wandb_params
    wandbobj["WANDB_PROJECT"] = project_name

    try:
        keyfile_content = get_keyfile_content("wandb")
        wandbobj["username"], wandbobj["key"] = keyfile_content
    except Exception as e:
        return e

    return wandbobj
