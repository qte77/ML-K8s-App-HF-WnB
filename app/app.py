#!/usr/bin/env python
"""Entrypoint for the app"""

from logging import debug
from sys import exit
from typing import Literal, Union

from helper.config_logger import config_logger_or_exit
from helper.parametrise_pipeline import get_param_dict
from helper.Pipeline import Pipeline


def main(mode: str = Union[Literal["train"], Literal["infer"]]) -> None:
    """
    Create pipeline object parametrised with parameter object and execute task.
    The task performed depends on the input of the `mode` [train, infer].
    """

    config_logger_or_exit()

    params = get_param_dict()

    debug(params)

    # pipeobj = Pipeline(get_param_dict())
    # pipeobj.do_prepare()
    # pipeobj.do_infer()
    # pipeobj.do_train()


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    exit(main())
