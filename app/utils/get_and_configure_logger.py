#!/usr/bin/env python
""""Load [logger_name] from [root]/[config_path]/[config_fn]"""

# TODO test whether error() gets thrown by root

from logging import getLogger
from logging.config import fileConfig
from os.path import abspath, dirname, exists, join, split

logger = getLogger(__name__)


def toggle_global_debug_state(show_debug: bool = False):
    """Toggle `global debug_on_global` to `debug_on`"""

    if show_debug:
        logger.debug(f"{__package__=}")

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
        logger.error("Can not find config. Exiting.")
        return FileNotFoundError

    try:
        fileConfig(abs_path)
    except Exception as e:
        logger.error(e)
        return e
