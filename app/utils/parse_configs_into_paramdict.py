#!/usr/bin/env python
"""Parse configs and return a parameter object"""
# TODO rename 'defaults' more specific and descriptive
# TODO generalize provider parametrisation
# TODO refactor Pipeline-object out into function only?
# TODO dataclass as code smell ?
# TODO dataclass and FP ?

from dataclasses import asdict, dataclass
from json import dump
from logging import getLogger
from os import environ as env
from typing import Union

from torch import device
from torch.cuda import is_available

from .configure_logging import debug_on_global
from .load_configs import (
    get_config_content,
    get_defaults,
    load_defaults_into_load_configs_module,
)

logger = getLogger(__name__)


@dataclass(repr=False, eq=False)
class ParamDict:
    """Holds structured parameter data."""

    dataset: dict[str, Union[str, list]]
    device: str
    metrics: dict[str, Union[dict[str, str], list]]
    model_name: str
    model_full_name: str
    project_name: str
    provider_env: dict[str, dict[str, str]]
    save_dir: str
    sweep: dict[str, Union[str, int, bool, dict]]


def get_param_dict() -> ParamDict:
    """
    Returns parameter dict with values filled with
    `helper.load_configs.get_config_content(<config>)`.

    Not Implemented yet: WANDB_NOTES, WANDB_TAGS, WANDB_MODE
    """

    if debug_on_global:
        logger.debug("Constructing parameter object as Type ParamDict")

    # TODO alters data and behavior of other class, no FP ?
    load_defaults_into_load_configs_module()

    hf_params = get_config_content("huggingface")
    task = get_config_content("task")
    task_model = hf_params["models"][task["model"]]

    paramdict = ParamDict(
        save_dir=get_defaults("save_dir"),
        sweep=_parse_sweep_config(get_config_content("sweep")),
        device=str(_get_device()),
        dataset=_parse_dataset_config(hf_params["datasets"], task["dataset"]),
        project_name="",
        model_name=task_model["name"],
        model_full_name=task_model["full_name"],
        metrics={},
        provider_env={},
    )

    paramdict.project_name = _create_project_name(
        task["model"],
        paramdict.dataset["dataset"],
        paramdict.device,
        paramdict.sweep["is_sweep"],
    )

    paramdict.metrics["metric_to_optimize"] = _parse_metric_to_optimize_config(
        hf_params["metrics_to_optimize"], task["metric_to_optimize"]
    )
    paramdict.metrics["metrics_to_load"] = _parse_metrics_to_load(
        hf_params["metrics_secondary_possible"], task["metrics_to_load"]
    )

    if paramdict.sweep["provider"] == "wandb":
        paramdict.provider_env = {}
        paramdict.provider_env["wandb"] = get_config_content("wandb")
        paramdict.provider_env["wandb"]["WANDB_PROJECT"] = paramdict.project_name

    if debug_on_global:
        _save_dict_to_file(asdict(paramdict))

    return paramdict


def _parse_dataset_config(datasets: dict, dataset: str) -> dict:
    """Gets the configuration of the dataset"""

    try:
        return datasets[dataset.lower()]
    except Exception as e:
        logger.error(e)
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
        logger.error(e)
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
        logger.error(e)
        return e


def _create_model_full_name(models: dict, model: str) -> str:
    """Loads the full name of the model"""

    try:
        return models.get(model.lower(), ["Invalid model", ""])["full_name"]
    except Exception as e:
        logger.error(e)
        return e


def _create_project_name(
    model: str, dataset_name: str, device: str, is_sweep: bool
) -> Union[str, Exception]:
    """Returns the project name as f'{model}-{dataset_name}-{device}{suffix}'"""

    suffix = "-sweep" if is_sweep else ""
    try:
        return f"{model}-{dataset_name}-{device}{suffix}".upper()
    except Exception as e:
        logger.error(e)
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
            logger.error(e)
            return e


def _save_dict_to_file(object_to_save: object, save_file: str = "./paramdict.json"):
    """Saves <paramdict>: ParamDict to [paramdict_file]: str"""

    logger.debug(f"Saving to '{save_file}' from {object_to_save=}")
    with open(save_file, "w") as outfile:
        dump(object_to_save, outfile, indent=2)
