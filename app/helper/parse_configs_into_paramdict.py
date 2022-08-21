#!/usr/bin/env python
"""Parse configs and return a parameter object"""
# TODO rename 'defaults' more specific and descriptive
# TODO generalize provider parametrisation
# TODO refactor Pipeline-object out into function only?
# TODO dataclass as code smell ?
# TODO dataclass and FP ?

from dataclasses import dataclass
from json import dump
from os import environ as env
from typing import Union

from torch import device
from torch.cuda import is_available

from .get_and_configure_logger import debug_on_global, get_and_configure_logger
from .load_configs import get_config_content, get_defaults, load_defaults

if debug_on_global:
    logger = get_and_configure_logger(__name__)
else:
    from logging import error


@dataclass(repr=False, eq=False)
class ParamDict:
    """
    Holds structured mutable data in the form of
    - `paramdict` as `dict[str, Union[str, list, dict]]`
    """

    paramdict: dict[
        str, Union[str, list[Union[str, list, dict]], dict[Union[str, list, dict]]]
    ]


def get_param_dict() -> ParamDict:
    """
    Returns parameter dict with values filled with
    `helper.load_configs.get_config_content(<config>)`.

    Not Implemented yet: WANDB_NOTES, WANDB_TAGS, WANDB_MODE
    """

    if debug_on_global:
        logger.debug("constructing parameter dictionary")

    # TODO alters data and behavior of other class, no FP ?
    load_defaults()

    hf_params = get_config_content("huggingface")
    task = get_config_content("task")
    task_model = hf_params["models"][task["model"]]

    pd = ParamDict
    pd.paramdict["save_dir"] = get_defaults()
    pd.paramdict["metrics"] = {}
    # paramdict["savedir"] =
    pd.paramdict["sweep"] = _parse_sweep_config(get_config_content("sweep"))
    pd.paramdict["device"] = str(_get_device())
    pd.paramdict["dataset"] = _parse_dataset_config(
        hf_params["datasets"], task["dataset"]
    )
    pd.paramdict["project_name"] = _create_project_name(
        task["model"],
        pd.paramdict["dataset"]["dataset"],
        pd.paramdict["device"],
        pd.paramdict["sweep"]["is_sweep"],
    )

    try:
        pd.paramdict["model_name"] = task_model["name"]
        pd.paramdict["model_full_name"] = task_model["full_name"]
    except Exception as e:
        logger.error(e) if debug_on_global else error(e)

    pd.paramdict["metrics"]["metric_to_optimize"] = _parse_metric_to_optimize_config(
        hf_params["metrics_to_optimize"], task["metric_to_optimize"]
    )
    pd.paramdict["metrics"]["metrics_to_load"] = _parse_metrics_to_load(
        hf_params["metrics_secondary_possible"], task["metrics_to_load"]
    )

    if pd.paramdict["sweep"]["provider"] == "wandb":
        pd.paramdict["wandb"] = get_config_content("wandb")
        pd.paramdict["wandb"]["WANDB_PROJECT"] = pd.paramdict["project_name"]

    if debug_on_global:
        paramdict_file = "./paramdict.json"
        logger.debug(f"Saving paramdict to '{paramdict_file}'")
        with open(paramdict_file, "w") as outfile:
            dump(pd.paramdict, outfile, indent=2)

    return pd


def _parse_dataset_config(datasets: dict, dataset: str) -> dict:
    """Gets the configuration of the dataset"""

    try:
        return datasets[dataset.lower()]
    except Exception as e:
        logger.error(e) if debug_on_global else error(e)
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
        logger.error(e) if debug_on_global else error(e)
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
    metrics_secondary_possible: list[str], metrics_to_load: list[str]
) -> list:
    """Loads secondary metrices"""

    try:
        return [met for met in metrics_to_load if met in metrics_secondary_possible]
    except Exception as e:
        logger.error(e) if debug_on_global else error(e)
        return e


def _create_model_full_name(models: dict, model: str) -> str:
    """Loads the full name of the model"""

    try:
        return models.get(model.lower(), ["Invalid model", ""])["full_name"]
    except Exception as e:
        logger.error(e) if debug_on_global else error(e)
        return e


def _create_project_name(
    model: str, dataset_name: str, device: str, is_sweep: bool
) -> Union[str, Exception]:
    """Returns the project name as f'{model}-{dataset_name}-{device}{suffix}'"""

    suffix = "-sweep" if is_sweep else ""
    try:
        return f"{model}-{dataset_name}-{device}{suffix}".upper()
    except Exception as e:
        logger.error(e) if debug_on_global else error(e)
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
            logger.error(e) if debug_on_global else error(e)
            return e
