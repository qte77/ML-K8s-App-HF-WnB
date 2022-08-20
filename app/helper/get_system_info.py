#!/usr/bin/env python
"""Returns information regarding the system the app is running on"""

from os import environ as env
from subprocess import check_output
from typing import Final

if "APP_DEBUG_IS_ON" in env:
    from logging import Logger

    from .configure_logger import configure_logger

    logger: Logger = configure_logger()

    global debug_on_global
    debug_on_global: Final = True


def get_system_info() -> list[str]:
    """Returns information regarding the system the app is running on"""
    # TODO import nv-smi etc

    if debug_on_global:
        logger.debug("Collecting system information")

    return check_output(["systeminfo"]).decode("utf-8").split("\r\n")
