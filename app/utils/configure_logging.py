#!/usr/bin/env python
""""
Offers logging facilities.

- Load [logger_name] from [root]/[config_path]/[config_fn]
- Logging functions `logger`, `metrics`, `analytics`
"""

from logging import getLogger, root
from logging.config import fileConfig
from os.path import abspath, dirname, exists, join, split
from sys import _getframe
from typing import Final

logger_cfglog = getLogger(__name__)
logging_types: Final = {
    "log": "debug",
    "warn": "warning",
    "error": "error",
    "metrics": "debug",
    "analytics": "debug",
}


def toggle_global_debug_state(show_debug: bool = False):
    """Toggle `global debug_on_global` to `debug_on`"""

    if show_debug:
        logger_cfglog.debug(f"{__package__=}")

    global debug_on_global
    debug_on_global = show_debug


def configure_logger(config_fn: str = "logging.conf", config_path: str = "config"):
    """Loads o logger configuration from the provided config file.

    The path to the config is constructed from 'root/[config_path]/[config_fn]'.
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
        logger_cfglog.error("Can not find config. Exiting.")
        return FileNotFoundError

    try:
        fileConfig(abs_path)
    except Exception as e:
        logger_cfglog.exception(e)
        return e


def logging_facility(log_type: str, log_message: str):
    """
    TODO Description: Offers logging.
    """

    try:
        _check_log_type_is_valid(log_type)
        caller = _getframe(1).f_globals["__name__"]

        if caller not in root.manager.loggerDict.keys():
            _create_logger_in_root_dict(caller)

        _log_by_name_and_type(caller, log_type, log_message)

    except Exception as e:
        logger_cfglog.exception(e)
        return e


def _check_log_type_is_valid(log_type) -> bool:
    """
    TODO Description
    """

    log_type_is_valid = log_type in logging_types.keys()

    if not log_type_is_valid:
        logger_cfglog.error("log_type not in logging_types.keys")

    return log_type_is_valid


def _create_logger_in_root_dict(logger_name: str):
    """
    TODO Description: Logs with dynamic logger and creates logger if not present
    """

    getLogger(logger_name)


# FIXME use other way to dynamically call logger functions
# use logger.adapter() instead of eval ?
# https://towardsdatascience.com/8-advanced-python-logging-features-that-you-shouldnt-miss-a68a5ef1b62d
def _log_by_name_and_type(logger_name: str, log_type: str, log_message: str):
    """
    TODO Description: Logs with dynamic logger and creates logger if not present
    """

    try:
        _check_log_type_is_valid(log_type)
        logger = f"root.manager.loggerDict[{logger_name}]"
        eval(f'{logger}.{logging_types[log_type]}("str({log_message})")')
    except Exception as e:
        logger_cfglog.exception(e)
        return e
