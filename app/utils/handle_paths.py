#!/usr/bin/env python
"""Exposes functions to handle paths"""

from os import makedirs
from os.path import (
    basename,
    dirname,
    exists,
    expanduser,
    join,
    normpath,
    realpath,
    splitext,
)
from typing import Union

from .handle_logging import logging_facility


def sanitize_path(path_to_sanitize: str = "~") -> Union[dict[str, str], Exception]:
    """
    Expands directory name '~' to $HOME if given and returns OS-specific path
    in the form of: { "dir": str, "base": str, "ext": str }
    """

    try:
        pth = normpath(realpath(expanduser(path_to_sanitize).replace("\\", "/")))
        pth_lst = [dirname(pth)] + list(splitext(basename(pth)))
        return {k: v for (k, v) in zip(["dir", "base", "ext"], pth_lst)}
    except Exception as e:
        logging_facility("exception", e)
        return e


def check_path(path_to_check: str) -> bool:
    """Checks whether a path exists"""

    try:
        return exists(join_path(path_to_check))
    except Exception as e:
        logging_facility("exception", e)
        return e


def create_path(dir_to_create: str):
    """Creates a path. Does nothing if path already exists."""

    try:
        makedirs(join_path(dir_to_create))
    except OSError:
        logging_facility("exception", OSError)
        pass
    except Exception as e:
        logging_facility("exception", e)
        return e


def join_path(path_to_join: str):
    """TODO"""

    dir = sanitize_path(path_to_join)
    return join(dir["dir"], dir["base"])
