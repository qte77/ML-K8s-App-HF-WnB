#!/usr/bin/env python
"""Entrypoint for the app"""

from os import environ as env
from typing import Final, NoReturn

if "APP_DEBUG_IS_ON" in env:
    from logging import debug, Logger
    from .helper.configure_logger import configure_logger
    from .helper.get_system_info import get_system_info

from .helper.parse_configs_into_paramdict import get_param_dict
from .helper.prepare_ml_input import prepare_pipeline

# from .model.infer_model import infer_model
# from .model.train_model import train_model

APP_MODES: Final = ["train", "infer"]


def main(mode: APP_MODES = "train") -> NoReturn:
    """
    Create pipeline object parametrised with parameter object and execute task.
    The task performed depends on the input of the
    `APP_MODES: Final = ["train", "infer"]`.\n
    Gets dateset and model from Hugging Face if not locally cached.\n
    Downloads the Metrics Builder Scripts from HF and returns their objects.\n
    Sets the environment variables the sweep provider needs.
    """

    # TODO remove mode check with pydantic
    if mode not in APP_MODES:
        mode = "train"

    if "APP_DEBUG_IS_ON" in env:
        logger: Logger = configure_logger()
        debug(f"App is running in {mode=}")
        debug(f"Debug is set to {logger=}")
        for item in get_system_info():
            debug(item)

    # paramobj = prepare_pipeline(get_param_dict())
    prepare_pipeline(get_param_dict())

    # _ = train_model(paramobj) if (mode == "train") else infer_model(paramobj)
