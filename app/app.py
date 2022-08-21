#!/usr/bin/env python
"""Entrypoint for the app"""

from sys import path
from typing import Literal

from .helper.get_and_configure_logger import debug_on_global, get_and_configure_logger
from .helper.get_and_configure_system_info import debug_system_info, show_sysinfo_global
from .helper.parse_configs_into_paramdict import get_param_dict
from .helper.prepare_ml_input import PipelineOutput, prepare_pipeline

if debug_on_global or show_sysinfo_global:
    logger = get_and_configure_logger(__name__)

# from .model.infer_model import infer_model
# from .model.train_model import train_model


def main(mode: Literal["train", "infer"] = "train") -> None:
    """
    Create pipeline object parametrised with parameter object and execute task.

    - Gets dateset and model from Hugging Face if not locally cached
    - Downloads the Metrics Builder Scripts from HF and returns their objects
    - Sets the environment variables the sweep provider needs
    - The task performed depends on the input of the

    Expects
    - `mode` as `Literal["train", "infer"]`
    """

    if debug_on_global:
        logger.debug(f"{path[0]=}, {__package__=}")
        logger.debug(f"{mode=}, {debug_on_global=}, {show_sysinfo_global=}")

    if show_sysinfo_global:
        debug_system_info()

    # pipeline_objects: Pipeline_Output = prepare_pipeline(get_param_dict())
    _: PipelineOutput = prepare_pipeline(get_param_dict())

    # _ = (
    #     train_model(**pipeline_objects)
    #     if (mode == "train")
    #     else infer_model(**pipeline_objects)
    # )
