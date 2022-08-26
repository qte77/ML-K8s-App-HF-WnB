#!/usr/bin/env python
"""
Sets state of the app and redirects to the entrypoint.

The state of the app is comprised of
- App mode, i.e. ["train"|"infer"]
- Global state of logging
- Showing system information
"""

from logging import getLogger
from sys import exit

from .utils.configure_logging import configure_logger, toggle_global_debug_state
from .utils.get_and_configure_system_info import toggle_global_sysinfo
from .utils.parse_args import parse_args

if __name__ == "__main__":

    app_mode, show_debug, show_sysinfo = parse_args()

    try:
        configure_logger()
        toggle_global_debug_state(show_debug)
        toggle_global_sysinfo(show_sysinfo)
    except Exception as e:
        exit(getLogger(__name__).error(e))

    # FIXME delayed import to account for logger set to be first
    from .app import main

    exit(main(app_mode))

else:
    msg = "Not inside __main__. Exiting."
    exit(getLogger(__name__).error(msg))
