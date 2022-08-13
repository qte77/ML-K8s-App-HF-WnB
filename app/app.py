#!/usr/bin/env python
"""Entrypoint for the app"""

from logging import debug
from sys import exit
from typing import Literal, Optional

from .helper.config_logger import config_logger
from .helper.get_system_info import get_system_info
from .helper.load_configs import set_debug_state_cfg
from .helper.parse_configs_into_paramdict import get_param_dict, set_debug_state_parse
from .helper.prepare_ml_input import (
    get_dataset,
    get_metrics_to_load_objects,
    get_model,
    set_debug_state_ml,
    set_provider_env,
)

# from .model.infer_model import infer_model
# from .model.train_model import train_model

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

    config_logger()

    if debug_on:
        debug(f"{debug_on=}, app running in {mode=}")
        debug(f"{get_system_info()=}")
        set_debug_state_cfg(debug_on)
        set_debug_state_ml(debug_on)
        set_debug_state_parse(debug_on)

    paramobj: dict = get_param_dict()
    paramobj["dataset"]["num_labels"] = get_dataset(
        paramobj["dataset"], paramobj["model_full_name"]
    )
    paramobj["metrics"]["metrics_loaded"] = get_metrics_to_load_objects(
        paramobj["metrics"]["metrics_to_load"]
    )
    get_model(paramobj["model_full_name"], paramobj["dataset"]["num_labels"])
    provider = paramobj["sweep"]["provider"]
    set_provider_env(provider, paramobj[provider])

    # if mode not in ["train", "infer"]:
    #     mode = "train"
    # _ = train_model(paramobj) if (mode == "train") else infer_model(paramobj)


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    exit(main())
