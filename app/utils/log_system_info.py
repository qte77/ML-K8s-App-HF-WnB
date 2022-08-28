#!/usr/bin/env python
"""Returns information regarding the system the app is running on"""


from os import environ, linesep
from os.path import join
from platform import architecture, uname
from subprocess import check_output

from .handle_logging import logging_facility


# TODO import nv-smi etc
def log_system_info():
    """Returns information regarding the system the app is running on"""

    system = uname()
    arch = architecture()

    logging_facility("log", f"{system=}, {arch=}")

    if system.system == "Windows":
        _log_windows_sysinfo(arch[0])


def _log_windows_sysinfo(architecture: str):
    # TODO docstring

    # TODO prettify debug output
    # .split(linesep) to output each line separate
    sysinfo_path = join(
        environ["SystemRoot"],
        "SysNative" if architecture == "32bit" else "System32",
        "systeminfo.exe",
    )
    try:
        sysinfo = check_output(sysinfo_path).decode("utf-8").split(linesep)
        for line in sysinfo:
            logging_facility("log", line)
    except Exception as e:
        logging_facility("exception", e)
        return e
