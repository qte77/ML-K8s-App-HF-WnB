#!/usr/bin/env python
"""Returns information regarding the system the app is running on"""

from subprocess import check_output

from .get_and_configure_logger import get_and_configure_logger

logger = get_and_configure_logger(__name__)


def toggle_global_sysinfo(show_sysinfo: bool = False):
    """Toggle `global debug_on_global` to `debug_on`"""

    global show_sysinfo_global
    show_sysinfo_global = show_sysinfo


def debug_system_info():
    """Returns information regarding the system the app is running on"""
    # TODO import nv-smi etc

    logger.debug("Collecting system information")

    try:
        # .split("\r\n")) to output each line separate
        logger.debug(check_output(["systeminfo"]).decode("utf-8"))
    except Exception as e:
        logger.error(e)
        return e
