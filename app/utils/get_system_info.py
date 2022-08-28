#!/usr/bin/env python
"""Returns information regarding the system the app is running on"""


from os import environ, linesep
from os.path import join
from platform import architecture, uname
from subprocess import check_output

from .handle_logging import logging_facility


# TODO import nv-smi etc
def get_system_info():
    """Returns information regarding the system the app is running on"""

    system = uname()
    arch = architecture()

    logging_facility("log", f"{system=}, {arch=}")

    if system.system == "Windows":
        # TODO prettify debug output
        # .split(linesep) to output each line separate
        sysinfo_path = join(
            environ["SystemRoot"],
            "SysNative" if arch[0] == "32bit" else "System32",
            "systeminfo.exe",
        )
        try:
            return check_output(sysinfo_path).decode("utf-8").split(linesep)
        except Exception as e:
            logging_facility("exception", e)
            return e
