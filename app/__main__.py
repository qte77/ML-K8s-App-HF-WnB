#!/usr/bin/env python
"""Redirects to entrypoint of the app"""

from os import environ as env
from sys import argv, exit

if True:
    from .helper.configure_logger import set_global_debug_state_and_logger

    set_logger = True if argv[1:2] and (argv[1:2])[0].lower() == "true" else False
    env["APP_DEBUGGER_ON"] = str(set_logger)
    set_global_debug_state_and_logger(set_logger)

    if argv[2:3] and (argv[2:3])[0].lower() == "true":
        env["APP_SHOW_SYSINFO"] = "set_this_to_None_if_not_needed"

from .app import main

if __name__ == "__main__":
    exit(main())
