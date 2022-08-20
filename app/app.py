#!/usr/bin/env python
"""Entrypoint for the app"""

from os import environ as env
from typing import Final

if "APP_DEBUG_IS_ON" in env:
    from logging import Logger

    from .helper.configure_logger import configure_logger
    from .helper.get_system_info import get_system_info

    logger: Logger = configure_logger()

    global debug_on_global
    debug_on_global: Final = True

from .helper.parse_configs_into_paramdict import get_param_dict
from .helper.prepare_ml_input import PipelineOutput, prepare_pipeline

# from .model.infer_model import infer_model
# from .model.train_model import train_model

APP_MODES: Final = ["train", "infer"]


def main(mode: APP_MODES = "train") -> None:
    """
    Create pipeline object parametrised with parameter object and execute task.

    - Gets dateset and model from Hugging Face if not locally cached
    - Downloads the Metrics Builder Scripts from HF and returns their objects
    - Sets the environment variables the sweep provider needs
    - The task performed depends on the input of the
    `APP_MODES: Final = ["train", "infer"]`.
    """

    # TODO remove mode check with pydantic
    if mode not in APP_MODES:
        mode = "train"

    if debug_on_global:
        logger.debug(f"App is running in {mode=}")
        logger.debug(f"Debug is set to {logger=}")
        if "APP_SHOW_SYSINFO" in env:
            for item in get_system_info():
                logger.debug(item)

    # pipeline_objects: Pipeline_Output = prepare_pipeline(get_param_dict())
    _: PipelineOutput = prepare_pipeline(get_param_dict())

    # _ = (
    #     train_model(**pipeline_objects)
    #     if (mode == "train")
    #     else infer_model(**pipeline_objects)
    # )
