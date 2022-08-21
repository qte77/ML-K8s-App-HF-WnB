#!/usr/bin/env python
"""Redirects to entrypoint of the app"""


def _parse_args() -> tuple[str, bool, bool]:
    """
    Parses argv and returns the inputs.

    Returns tuple of
    - String of app mode out of `["train", "infer"]`
    - Tuple of bools to output debug and/or sysinfo
    """

    desc = "Create pipeline object parametrised with parameter object and execute task."
    modes = ["train", "infer"]

    parser = ArgumentParser(prog="app", description=desc)
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default=modes[0],
        choices=modes,
        help="change app mode",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="show debug messages"
    )
    parser.add_argument(
        "-i", "--sysinfo", action="store_true", help="show system information"
    )
    args = parser.parse_args()

    return (args.mode, args.debug, args.sysinfo)


def _set_global_state(show_debug: bool = False, show_sysinfo: bool = False):
    """TODO"""

    try:
        toggle_global_debug_state(show_debug)
        toggle_global_sysinfo(show_sysinfo)
    except Exception as e:
        get_and_configure_logger(__name__).error(e)
        return e


if __name__ == "__main__":

    from argparse import ArgumentParser
    from sys import exit

    from .helper.get_and_configure_logger import (
        get_and_configure_logger,
        toggle_global_debug_state,
    )
    from .helper.get_and_configure_system_info import toggle_global_sysinfo

    app_mode, show_debug, show_sysinfo = _parse_args()
    _set_global_state(show_debug, show_sysinfo)

    # delayed import to account for logger set to be first
    from .app import main

    exit(main(app_mode))
