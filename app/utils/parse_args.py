#!/usr/bin/env python
"""Handles arguments to the app"""

from argparse import ArgumentParser


def parse_args() -> tuple[str, bool, bool]:
    """
    Parses and evaluates argv and returns the results.

    Returns tuple of
    - String of app mode out of `["train", "infer"]`
    - Bools for global logging and/or showing system information
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
