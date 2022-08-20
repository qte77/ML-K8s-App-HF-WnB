#!/usr/bin/env python
"""Returns information regarding the system the app is running on"""

from subprocess import check_output

from .configure_logger import debug_on_global, logger_global


def get_system_info() -> list[str]:
    """Returns information regarding the system the app is running on"""
    # TODO import nv-smi etc

    if debug_on_global:
        logger_global.debug("Collecting system information")

    return check_output(["systeminfo"]).decode("utf-8").split("\r\n")
