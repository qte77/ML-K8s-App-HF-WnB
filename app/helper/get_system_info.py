#!/usr/bin/env python
"""Returns information regarding the system the app is running on"""

from subprocess import check_output

from .get_and_configure_logger import get_and_configure_logger

logger = get_and_configure_logger(__name__)


def debug_system_info():
    """Returns information regarding the system the app is running on"""
    # TODO import nv-smi etc

    logger.debug("Collecting system information")

    try:
        for item in check_output(["systeminfo"]).decode("utf-8").split("\r\n"):
            logger.debug(item)
    except Exception as e:
        logger.error(e)
        return e
