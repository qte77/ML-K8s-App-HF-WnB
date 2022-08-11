#!/usr/bin/env python
"""Entrypoint for the app"""

from json import dump
from logging import debug
from sys import exit
from typing import Literal

from .helper.config_logger import config_logger
from .helper.parametrise_pipeline import get_param_dict, set_debug_on_pipeline
from .helper.Pipeline import Pipeline
from .model.infer_model import infer_model
from .model.train_model import train_model

# modes = Literal["train", "infer"]


def main(mode: Literal["train", "infer"] = "train", debug_on: bool = False) -> None:
    """
    Create pipeline object parametrised with parameter object and execute task.
    The task performed depends on the input of the `mode` [train, infer].
    """

    if mode not in ["train", "infer"]:
        mode = "train"

    config_logger()
    set_debug_on_pipeline(debug_on)
    paramobj: dict = get_param_dict()

    if debug_on:
        paramobj_file = "./paramobj.json"
        debug(f"App in {mode=}")
        debug(f"Printing paramobj to {paramobj_file}")
        with open(paramobj_file, "w") as outfile:
            dump(paramobj, outfile, indent=2)

    pipeobj = Pipeline(paramobj)
    pipeobj.prepare_ml_external_components()

    train_model() if (mode == "train") else infer_model()


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    exit(main())
