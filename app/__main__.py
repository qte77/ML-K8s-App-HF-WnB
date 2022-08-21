#!/usr/bin/env python
"""Redirects to entrypoint of the app"""


def _parse_args() -> tuple[str, tuple[bool]]:
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

    return (args.mode, (args.debug, args.sysinfo))


def _set_global_state(show_debug: bool = False, show_sysinfo: bool = False):
    """TODO"""

    if show_sysinfo:
        env["APP_SHOW_SYSINFO"] = str(show_sysinfo)

    try:
        set_global_debug_state_and_logger(show_debug, show_sysinfo)
    except Exception as e:
        return e


if __name__ == "__main__":

    from argparse import ArgumentParser
    from os import environ as env
    from sys import exit

    from .helper.configure_logger import set_global_debug_state_and_logger

    app_mode, app_debug = _parse_args()
    _set_global_state(*app_debug)

    # late import to account for gloab vars set by configure_logger
    from .app import main

    exit(main(app_mode))
