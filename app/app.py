#!/usr/bin/env python
"""Entrypoint for the app"""

from sys import path
from typing import Literal

from .utils.configure_logging import debug_on_global, logging_facility
from .utils.get_and_configure_system_info import debug_system_info, show_sysinfo_global
from .utils.parse_configs_into_paramdict import get_param_dict
from .utils.prepare_ml_input import PipelineOutput, prepare_pipeline

# from .model.infer_model import infer_model
# from .model.train_model import train_model


def main(mode: Literal["train", "infer"] = "train"):
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
        logging_facility("log", f"{path[0]=}, {__package__=}")
        logging_facility(
            "metrics", f"{mode=}, {debug_on_global=}, {show_sysinfo_global=}"
        )

    if show_sysinfo_global:
        debug_system_info()

    # pipeline_objects: Pipeline_Output = prepare_pipeline(get_param_dict())
    _: PipelineOutput = prepare_pipeline(get_param_dict())

    # _ = (
    #     train_model(**pipeline_objects)
    #     if (mode == "train")
    #     else infer_model(**pipeline_objects)
    # )
