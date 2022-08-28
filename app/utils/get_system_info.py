#!/usr/bin/env python
"""Returns information regarding the system the app is running on"""


from os import linesep
from subprocess import check_output

from .handle_logging import logging_facility


# TODO import nv-smi etc
def get_system_info():
    """Returns information regarding the system the app is running on"""

    try:
        # FIXME codefactor malus for rel path, use abs path
        # win sysinfo, linux uname -a etc
        # TODO prettify debug output
        # .split(linesep) to output each line separate
        sysinfo_output = check_output(["systeminfo"]).decode("utf-8").split(linesep)
        return sysinfo_output
    except Exception as e:
        logging_facility("exception", e)
        return e
