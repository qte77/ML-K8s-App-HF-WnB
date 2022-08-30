#!/usr/bin/env python
"""
Sets state of the app and redirects to the entrypoint.

The state of the app is comprised of
- App mode, i.e. ["train"|"infer"]
- Global state of logging
- Showing system information
"""

from sys import exit, path

from .utils.handle_logging import (
    configure_logger,
    logging_facility,
    toggle_global_debug_state,
)
from .utils.log_system_info import log_system_info
from .utils.parse_args import parse_args

if True:
    toggle_pydantic: bool = True
    configure_logger()


def _log_basic_info():
    """
    TODO
    """

    [
        logging_facility("log", msg)
        for msg in [
            "Configuring app",
            f"{path[0]=}",
            f"{__package__=}",
            f"{mode=}, {debug_on=}, {sysinfo_on=}, {sysinfoexit_on=}",
        ]
    ]


def _toggle_global_debug(debug_on: bool):
    """
    TODO
    """

    try:
        toggle_global_debug_state(debug_on)
    except Exception as e:
        logging_facility("exception", e)
        return e


def _show_sysinfo():
    """
    TODO
    """

    logging_facility("log", "Collecting system information")

    try:
        log_system_info()
    except Exception as e:
        logging_facility("exception", e)
        return e


if __name__ == "__main__":

    mode, debug_on, sysinfo_on, sysinfoexit_on = parse_args().values()

    _toggle_global_debug(debug_on)

    if debug_on:
        _log_basic_info()

    if sysinfo_on or sysinfoexit_on:
        _show_sysinfo()
        if sysinfoexit_on:
            exit()

    # FIXME delayed import because of global debug toggle
    if True:
        from .utils.toggle_features import toggle_global_pydantic
    toggle_global_pydantic(toggle_pydantic)

    # FIXME delayed import because of global debug toggle
    from .app import app

    exit(app(mode=mode))

else:
    # FIXME exit before functions are loaded ?
    exit(logging_facility("error", "Not inside __main__. Exiting."))
