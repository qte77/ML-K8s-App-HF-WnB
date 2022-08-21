#!/usr/bin/env python
""""Load [logger_name] from [root]/[config_path]/[config_fn]"""

# TODO test whether error() gets thrown by root

from logging import Logger, getLogger, root
from logging.config import fileConfig
from os.path import abspath, dirname, exists, join, split


def toggle_global_debug_state(debug_on: bool = False):
    """Toggle `global debug_on_global` to `debug_on`"""

    global debug_on_global
    debug_on_global = debug_on


def toggle_global_sysinfo(show_sysinfo: bool = False):
    """Toggle `global debug_on_global` to `debug_on`"""

    global show_sysinfo_global
    show_sysinfo_global = show_sysinfo


def get_and_configure_logger(
    logger_name: str = "APP",
    config_fn: str = "logging.conf",
    config_path: str = "config",
) -> Logger:
    """
    Loads a logger from app/package root.

    - Configures the logger or exits if logger is not existing or error occurs
    - The logger with [logger_name] is loaded from the provided config file
    - The path to the config is constructed from 'root/[config_path]/[config_fn]'

    See Python documentation for [logging](\
https://docs.python.org/3/library/logging.html\
) and [logging.config.fileConfig](\
https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig\
) as well as the [Logging HOWTO](https://docs.python.org/3/howto/logging.html) and \
the [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html).
    """

    abs_path = split(dirname(abspath(__file__)))[0]
    abs_path = join(abs_path, config_path, config_fn)

    if not exists(abs_path):
        root.error("Can not find config. Exiting.")
        return FileNotFoundError

    try:
        fileConfig(abs_path)
        return getLogger(logger_name)
    except Exception as e:
        root.error(e)
        return e
