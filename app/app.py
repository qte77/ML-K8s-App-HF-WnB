#!/usr/bin/env python
"""Entrypoint for the app"""

from typing import Literal

# from .model.infer_model import infer_model
# from .model.train_model import train_model
from .utils.configure_logging import debug_on_global, logging_facility
from .utils.parse_configs_into_paramdict import get_param_dict
from .utils.prepare_ml_input import prepare_pipeline


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
        logging_facility("log", "Starting app")

    _ = prepare_pipeline(get_param_dict())
    # train_model(pipeobj) if (mode == "train") else infer_model(pipeobj)
