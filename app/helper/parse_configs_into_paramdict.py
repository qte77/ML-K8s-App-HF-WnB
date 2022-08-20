#!/usr/bin/env python
"""Parse configs and return a parameter object"""
# TODO rename 'defaults' more specific and descriptive
# TODO generalize provider parametrisation
# TODO refactor Pipeline-object out into function only?
# TODO dataclass as code smell ?
# TODO dataclass and FP ?

from dataclasses import dataclass
from json import dump
from logging import error
from os import environ as env
from typing import Final, Union

from torch import device
from torch.cuda import is_available

if "APP_DEBUG_IS_ON" in env:
    from logging import debug

    global debug_on_global
    debug_on_global: Final = True

from .load_configs import get_config_content, get_defaults, load_defaults


@dataclass(repr=False, eq=False)
class ParamDict:
    """
    Holds structured mutable data in the form of
    - `paramdict` as `dict[str, Union[str, list, dict]]`
    """

    paramdict: dict[str, Union[str, list, dict]]


def get_param_dict() -> ParamDict:
    """
    Returns parameter dict with values filled with
    `helper.load_configs.get_config_content(<config>)`
    Not Implemented yet: WANDB_NOTES, WANDB_TAGS, WANDB_MODE
    """

    # TODO alters data and behavior of other class, no FP ?
    load_defaults()

    hf_params: dict = get_config_content("huggingface")
    task: dict = get_config_content("task")
    task_model: dict = hf_params["models"][task["model"]]

    paramdict = {}
    paramdict["save_dir"] = get_defaults()
    paramdict["metrics"] = {}
    # paramdict["savedir"] =
    paramdict["sweep"]: dict = _parse_sweep_config(get_config_content("sweep"))
    paramdict["device"]: str = str(_get_device())
    paramdict["dataset"]: dict = _parse_dataset_config(
        hf_params["datasets"], task["dataset"]
    )
    paramdict["project_name"]: str = _create_project_name(
        task["model"],
        paramdict["dataset"]["dataset"],
        paramdict["device"],
        paramdict["sweep"]["is_sweep"],
    )

    try:
        paramdict["model_name"] = task_model["name"]
        paramdict["model_full_name"] = task_model["full_name"]
    except Exception as e:
        error(e)

    paramdict["metrics"]["metric_to_optimize"]: dict = _parse_metric_to_optimize_config(
        hf_params["metrics_to_optimize"], task["metric_to_optimize"]
    )
    paramdict["metrics"]["metrics_to_load"] = _parse_metrics_to_load(
        task["metrics_to_load"], hf_params["metrics_secondary_possible"]
    )

    if paramdict["sweep"]["provider"] == "wandb":
        paramdict["wandb"] = get_config_content("wandb")
        paramdict["wandb"]["WANDB_PROJECT"] = paramdict["project_name"]

    if debug_on_global:
        paramdict_file = "./paramdict.json"
        debug(f"Printing paramdict to '{paramdict_file}'")
        with open(paramdict_file, "w") as outfile:
            dump(paramdict, outfile, indent=2)

    return paramdict


def _parse_dataset_config(datasets: dict, dataset: str) -> dict:
    """Gets the configuration of the dataset"""

    try:
        return datasets[dataset.lower()]
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


def _parse_metrics_to_load(
    metrics_to_load: list[str], metrics_secondary_possible: list[str]
) -> list:
    """Loads secondary metrices"""

    try:
        return [met for met in metrics_to_load if met in metrics_secondary_possible]
    except Exception as e:
        return e


def _create_model_full_name(models: dict, model: str) -> str:
    """Loads the full name of the model"""

    try:
        return models.get(model.lower(), ["Invalid model", ""])["full_name"]
    except Exception as e:
        return e


def _create_project_name(
    model: str, dataset_name: str, device: str, is_sweep: bool
) -> Union[str, Exception]:
    """Returns the project name as f'{model}-{dataset_name}-{device}{suffix}'"""

    suffix = "-sweep" if is_sweep else ""
    try:
        return f"{model}-{dataset_name}-{device}{suffix}".upper()
    except Exception as e:
        return e


def _get_device() -> str:
    """Returns the device as 'cpu', 'cuda' or 'tpu'"""

    # TODO make it platform independent, TPU_NAME used by Google Colab
    if "TPU_NAME" in env:
        return "tpu"
    else:
        try:
            return device("cuda" if is_available() else "cpu")
        except Exception as e:
            return e
