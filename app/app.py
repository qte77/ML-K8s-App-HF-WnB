#!/usr/bin/env python
"""Entrypoint for the app"""

from json import dump
from logging import debug
from sys import exit
from typing import Literal, Optional

from .helper.config_logger import config_logger
from .helper.load_configs import set_debug_state_cfg
from .helper.parse_configs_into_paramobj import get_param_dict
from .helper.prepare_ml_input import (
    get_dataset,
    get_metrics_to_load_objects,
    get_model,
    set_debug_state_ml,
    set_provider_env,
)
from .model.infer_model import infer_model
from .model.train_model import train_model

# modes = Literal["train", "infer"]


def main(
    mode: Optional[Literal["train", "infer"]] = "train", debug_on: bool = False
) -> None:
    """
    Create pipeline object parametrised with parameter object and execute task.
    The task performed depends on the input of the `mode` Optional["train", "infer"].
    Gets dateset and model from Hugging Face if not locally cached.\n
    Downloads the Metrics Builder Scripts from HF and returns their objects.\n
    Sets the environment variables the sweep provider needs.
    """

    if mode not in ["train", "infer"]:
        mode = "train"

    config_logger()

    if debug_on:
        debug(f"{debug_on=}, app running in {mode=}")
        set_debug_state_cfg(debug_on)
        set_debug_state_ml(debug_on)

    paramobj: dict = get_param_dict()
    paramobj["dataset"]["num_labels"] = get_dataset(
        paramobj["dataset"], paramobj["model_full_name"]
    )
    get_model(paramobj["model_full_name"], paramobj["dataset"]["num_labels"])
    paramobj["metrics"]["metrics_to_load"] = get_metrics_to_load_objects(
        paramobj["metrics"]["metrics_to_load"]
    )
    provider = paramobj["sweep"]["provider"]
    set_provider_env(provider, paramobj[provider])

    if debug_on:
        paramobj_file = "./paramobj.json"
        debug(f"Printing paramobj to '{paramobj_file}'")
        with open(paramobj_file, "w") as outfile:
            dump(paramobj, outfile, indent=2)

    _ = train_model() if (mode == "train") else infer_model()


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    exit(main())


# def get_task(self) -> None:
#     return self.task


# def get_paramobj(self) -> object:
#     # TODO type hint as Pipeline or dict
#     return self.paramobj


# def get_sys_info() -> None:
#     # TODO unload module watermark
#     # TODO use build-in functionality to provide info?
#     # import watermark
#     # watermark -u -i -v -iv
#     return NotImplementedError
