#!/usr/bin/env python
"""Entrypoint for the app"""

from sys import exit
from typing import Literal, Union

from .helper.create_pipeline_object import Pipeline
from .helper.parametrise_pipeline import get_param_object


def main(mode: str = Union[Literal["train"], Literal["infer"]]) -> None:
    """
    Create pipeline object parametrised with parameter object and execute task.
    The task performed depends on the input of the `mode` [train, infer].
    """

    pipeobj = Pipeline(get_param_object())
    pipeobj.do_prepare()
    pipeobj.do_infer()
    pipeobj.do_train()


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    exit(main())
