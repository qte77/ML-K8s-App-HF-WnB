#!/usr/bin/env python
"""Exposes a function to sanitize paths"""

from os.path import basename, dirname, expanduser, normpath, realpath, splitext


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
