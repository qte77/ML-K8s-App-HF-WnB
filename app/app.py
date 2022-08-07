#!/usr/bin/env python
"""Entrypoint for the app"""

from json import dump
from sys import exit
from typing import Literal, Union

from helper.config_logger import config_logger
from helper.parametrise_pipeline import get_param_dict
from helper.Pipeline import Pipeline


def main(
    mode: str = Union[Literal["train"], Literal["infer"]],
    dbg_on: bool = False,
) -> None:
    """
    Create pipeline object parametrised with parameter object and execute task.
    The task performed depends on the input of the `mode` [train, infer].
    """

    config_logger()

    params: dict = get_param_dict()

    if dbg_on:
        with open("paramobj.json", "w") as outfile:
            dump(params, outfile, indent=2)

    pipeobj = Pipeline(params)
    pipeobj.prepare_ml_input()
    # pipeobj.do_infer()
    # pipeobj.do_train()


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    exit(main(dbg_on=False))
