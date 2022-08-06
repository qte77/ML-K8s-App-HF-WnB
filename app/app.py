#!/usr/bin/env python
"""Entrypoint for the app"""

from helper.create_pipeline_object import Pipeline
from helper.parametrise_pipeline import get_param_object


def main():
    """Create pipeline object parametrised with parameter object"""

    pipeobj = Pipeline(get_param_object())
    pipeobj.do_prepare()
    pipeobj.do_infer()
    pipeobj.do_train()


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    main()
