#!/usr/bin/env python
""""Load [logger_name] from [root]/[config_path]/[config_fn]"""

from logging import error, getLogger
from logging.config import fileConfig
from os.path import abspath, dirname, exists, join, split
from sys import exit


def config_logger_or_exit(
    logger_name: str = "simpleExample",
    config_fn: str = "logging.conf",
    config_path: str = "config",
) -> None:
    """
    Load [logger_name] from [root]/[config_path]/[config_fn]
    Configure the logger or exit if not existing or error occurs
    The path to the config is constructed from app/package root
    https://docs.python.org/3/library/logging.html
    https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig
    """

    abs_path = split(dirname(abspath(__file__)))[0]
    abs_path = join(abs_path, config_path, config_fn)

    if not exists(abs_path):
        error("Can not find config. Exiting.")
        exit()

    # TODO simpleExample not loaded from logging.conf
    try:
        fileConfig(abs_path)
        getLogger(logger_name)
    except Exception as e:
        error(e)
        exit()
