#!/usr/bin/env python
"""Returns information regarding the system the app is running on"""

from subprocess import check_output


def get_system_info() -> list[str]:
    """Returns information regarding the system the app is running on"""
    # TODO import nv-smi etc
    return check_output(["systeminfo"]).decode("utf-8").split("\r\n")
