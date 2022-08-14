#!/usr/bin/env python
"""Redirects to entrypoint of the app"""

from os import environ as env
from sys import exit

# TODO conditional imports and env best practices, maybe use parsed .env with dotenv
# conditional to avoid flake8 E402 module level import not at top of file
if True:
    env["APP_DEBUG_IS_ON"] = "True"
    # env["APP_SHOW_SYSINFO"] = "True"

from .app import main

if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    exit(main())
