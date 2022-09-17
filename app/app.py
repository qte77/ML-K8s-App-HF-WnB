#!/usr/bin/env python
"""Entrypoint for the app"""

from enum import Enum

# from .payload.infer_model import infer_model
# from .payload.train_model import train_model
from .pipeline.prepare_pipe_data import prepare_pipe_data
from .pipeline.prepare_pipe_params import get_parameters
from .utils.handle_logging import debug_on_global, logging_facility


class AppModes(Enum):
    """Enum for possible modes the app can run in"""

    train = "train"
    infer = "infer"


def app(mode: AppModes = AppModes.train):
    """
    Create pipeline object parametrised with parameter object and execute task.

    - Gets dateset and model from Hugging Face if not locally cached
    - Downloads the Metrics Builder Scripts from HF and returns their objects
    - Sets the environment variables the sweep provider needs
    - The task performed depends on the input of the

    Expects
    - `mode` as `AppMode`
    """

    if debug_on_global:
        logging_facility("log", "Starting app")

    _ = prepare_pipe_data(get_parameters())  # pipedata
    # train_model(pipedata) if (mode == "train") else infer_model(pipedata)
