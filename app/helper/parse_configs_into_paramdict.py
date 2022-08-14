#!/usr/bin/env python
"""Parse configs and return a parameter object"""
# TODO rename 'defaults' more specific and descriptive
# TODO generalize provider parametrisation
# TODO refactor Pipeline-object out into function only?

# from logging import debug
from json import dump
from os import environ as env
from typing import Union

if "APP_DEBUG_IS_ON" in env:
    from logging import debug

from torch import device
from torch.cuda import is_available

from .load_configs import get_config_content, get_defaults, load_defaults


def get_param_dict() -> dict:
    """
    Returns parameter dict with values filled with
    `helper.load_configs.get_config_content(<config>)`
    Not Implemented yet: WANDB_NOTES, WANDB_TAGS, WANDB_MODE
    """

    load_defaults()
    hf_params: dict = get_config_content("huggingface")
    task: dict = get_config_content("task")
    paramobj = {}
    paramobj["save_dir"] = get_defaults()
    paramobj["metrics"] = {}
    # paramobj["savedir"] =
    paramobj["sweep"]: dict = _parse_sweep_config(get_config_content("sweep"))
    paramobj["device"]: str = str(_get_device())
    paramobj["dataset"]: dict = _parse_dataset_config(
        hf_params["datasets"], task["dataset"]
    )
    paramobj["project_name"]: str = _create_project_name(
        task["model"],
        paramobj["dataset"]["dataset"],
        paramobj["device"],
        paramobj["sweep"]["is_sweep"],
    )
    paramobj["model_full_name"]: str = _create_model_full_name(
        hf_params["models"], task["model"]
    )
    paramobj["metrics"]["metric_to_optimize"]: dict = _parse_metric_to_optimize_config(
        hf_params["metrics_to_optimize"], task["metric_to_optimize"]
    )
    paramobj["metrics"]["metrics_to_load"] = _parse_metrics_to_load(
        task["metrics_to_load"], hf_params["metrics_secondary_possible"]
    )

    if paramobj["sweep"]["provider"] == "wandb":
        paramobj["wandb"] = get_config_content("wandb")
        # TODO wandb docu for env var names used for API access
        paramobj["wandb"]["WANDB_PROJECT"] = paramobj["project_name"]

    if "APP_DEBUG_IS_ON" in env:
        paramobj_file = "./paramobj.json"
        debug(f"Printing paramobj to '{paramobj_file}'")
        with open(paramobj_file, "w") as outfile:
            dump(paramobj, outfile, indent=2)

    return paramobj


def _parse_dataset_config(datasets: dict, dataset: str) -> dict:
    """Gets the configuration of the dataset"""

    try:
        return datasets[dataset.lower()]
    except Exception as e:
        return e


def _create_model_full_name(models: dict, model: str) -> str:
    """Loads the full name of the model"""

    try:
        return models.get(model.lower(), ["Invalid model", ""])
    except Exception as e:
        return e


def _parse_metric_to_optimize_config(
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


def _parse_metrics_to_load(
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
    if "TPU_NAME" in env:
        return "tpu"
    else:
        try:
            return device("cuda" if is_available() else "cpu")
        except Exception as e:
            return e


def _create_project_name(
    model: str, dataset_name: str, device: str, is_sweep: bool
) -> Union[str, Exception]:
    """Returns the project name as f'{model}-{dataset_name}-{device}{suffix}'"""

    suffix = "-sweep" if is_sweep else ""
    try:
        return f"{model}-{dataset_name}-{device}{suffix}"
    except Exception as e:
        return e


def _parse_sweep_config(sweep: dict) -> dict:
    """Gets the configuration of the sweep"""

    sweepobj = {}
    sweepobj["is_sweep"] = True if int(sweep["train_count"]) > 1 else False

    if sweepobj["is_sweep"]:
        sweep_provider = sweep["provider"]
        sweepobj["provider"] = sweep_provider
        sweepobj["config"] = get_config_content(f"sweep-{sweep_provider}")
        sweepobj["train_count"] = sweep["train_count"]

    return sweepobj
