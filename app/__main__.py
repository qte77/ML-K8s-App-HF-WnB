#!/usr/bin/env python
"""
Sets state of the app and redirects to the entrypoint.

The state of the app is comprised of
- App mode, i.e. ["train"|"infer"]
- Global state of logging
- Showing system information
"""

from sys import exit, path

from .utils.configure_logging import (
    configure_logger,
    logging_facility,
    toggle_global_debug_state,
)
from .utils.get_system_info import get_system_info
from .utils.parse_args import parse_args

configure_logger()


def _log_basic_info():
    """TODO"""

    logging_facility("log", "Configuring app")
    logging_facility("log", f"{path[0]=}, {__package__=}")
    logging_facility("log", f"{mode=}, {debug_on=}, {sysinfo_on=}, {sysinfoexit_on=}")


def _toggle_global_debug(debug_on: bool):
    """TODO"""

    try:
        toggle_global_debug_state(debug_on)
    except Exception as e:
        debug_on = False
        logging_facility("exception", e)


def _show_sysinfo():
    """TODO"""

    logging_facility("log", "Collecting system information")
    try:
        logging_facility("log", get_system_info())
    except Exception as e:
        logging_facility("exception", e)


if __name__ == "__main__":

    mode, debug_on, sysinfo_on, sysinfoexit_on = parse_args().values()

    if debug_on:
        _log_basic_info()
    _toggle_global_debug(debug_on)

    if sysinfo_on or sysinfoexit_on:
        _show_sysinfo()
        if sysinfoexit_on:
            exit()

    # FIXME delayed import to account for logger set to be first
    from .app import main

    exit(main(mode))

else:

    exit(logging_facility("error", "Not inside __main__. Exiting."))
