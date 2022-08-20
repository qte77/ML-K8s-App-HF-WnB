#!/usr/bin/env python
""""Load [logger_name] from [root]/[config_path]/[config_fn]"""

from logging import Logger, debug, error, getLogger
from logging.config import fileConfig
from os.path import abspath, dirname, exists, join, split


def set_global_debug_state_and_logger(debug_on: bool = False):
    """Toggle global debug state and set global logger"""

    if debug_on is not True:
        debug_on = False

    debug(f"{debug_on=}")

    _toggle_global_debug_state(debug_on)
    _set_global_logger(debug_on)


def _toggle_global_debug_state(debug_on: bool = False):
    """Toggle `global debug_on_global` to `debug_on`"""

    global debug_on_global
    debug_on_global = debug_on


def _set_global_logger(debug_on: bool = False):
    """
    Set `global logger_global` relative to `debug_on`.

    - `False`: `None`
    - `True`: `Logger`
    """

    global logger_global
    logger_global = _configure_and_get_logger() if debug_on else None


def _configure_and_get_logger(
    logger_name: str = "APP",
    config_fn: str = "logging.conf",
    config_path: str = "config",
) -> Logger:
    """
    Loads a logger from app/package root.

    - Configures the logger or exits if logger is not existing or error occurs
    - The logger with [logger_name] is loaded from the provided config file
    - The path to the config is constructed from 'root/[config_path]/[config_fn]'

    See Python documenatation for [logging](\
https://docs.python.org/3/library/logging.html\
) and [logging.config.fileConfig](\
https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig\
).
    """

    abs_path = split(dirname(abspath(__file__)))[0]
    abs_path = join(abs_path, config_path, config_fn)

    if not exists(abs_path):
        error("Can not find config. Exiting.")
        return FileNotFoundError

    # TODO simpleExample not loaded from logging.conf
    try:
        fileConfig(abs_path)
        return getLogger(logger_name)
    except Exception as e:
        error(e)
        return e
