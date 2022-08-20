#!/usr/bin/env python
"""Exposes a function to sanitize paths"""

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


def sanitize_path(path_to_sanitize: str = "~") -> dict[str, str]:
    """
    Expands directory name '~' to $HOME if given and returns OS-specific path\n
    in the form of: { "dir": str, "base": str, "ext": str }
    """

    try:
        pth = normpath(realpath(expanduser(path_to_sanitize).replace("\\", "/")))
        pth_lst = [dirname(pth)] + list(splitext(basename(pth)))
        return {k: v for (k, v) in zip(["dir", "base", "ext"], pth_lst)}
    except Exception as e:
        return e


def check_and_create_path(path_to_check: str) -> tuple[str, bool]:
    """
    Checks whether a path exists and creates it if not.
    Returns (joined path, bool path exists).
    """

    dir = sanitize_path(path_to_check)
    dir_path = join(dir["dir"], dir["base"])

    try:
        if not exists(dir_path):
            makedirs(dir_path)
            return (dir_path, False)
        else:
            return (dir_path, True)
    except Exception as e:
        return e
