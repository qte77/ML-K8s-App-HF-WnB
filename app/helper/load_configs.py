#!/usr/bin/env python
"""
Load configuration files
TODO some error checks missing
"""

from logging import debug, error
from os.path import abspath, dirname, exists, expanduser, join, split
from typing import Literal, Union

from yaml import safe_load


def set_debug_state_cfg(debug_on: bool = False):
    global debug_on_glob
    debug_on_glob = debug_on


def get_config_content(cfg_name: str) -> dict:
    """Returns config objects"""

    if debug_on_glob:
        defaults_dbg_msg = f"'{cfg_name}' found in defaults."
        # TODO test case and type
        if _check_or_get_default("config_fn", cfg_name):
            debug(defaults_dbg_msg)
        else:
            debug(f"No {defaults_dbg_msg} Trying to find the file anyway.")

    return _load_yml(cfg_name)


def _sanitize_path(path: str = "~") -> str:
    """Expands '~' to $HOME if given and returns OS-specific path"""

    if "\\" in path:
        path = path.replace("\\", "/")
    if path.startswith("~"):
        path = expanduser(path)

    return join(*path.split("/"))


def get_default_save_dir() -> dict:
    """Looks for 'save_dir' inside 'defaults.yml' and returns it if found"""

    return _sanitize_path(_check_or_get_default("save_dir", mode_check_get="get"))


def get_keyfile_content(provider: str = "wandb") -> dict:
    """
    Returns keyfile objects
    TODO generalize path split
    """

    try:
        keyfile_full = _check_or_get_default("keyfiles", provider, mode_check_get="get")
        # TODO generalize path split
        kf_path_fn = keyfile_full.rsplit("/", 1)
        return _load_yml(kf_path_fn[1], kf_path_fn[0])
    except Exception as e:
        return e


def _check_or_get_default(
    cfg_keyname: str,
    cfg_value_to_search: str = None,
    cfg_defaults_fn: str = "defaults",
    cfg_path: str = "config",
    mode_check_get: Literal["check", "get"] = "check",
) -> Union[bool, str]:
    """
    Returns the standard configuration file names placed under
    [cfg_keyname] found in [cfg_path]/[cfg_defaults].yml
    """

    # TODO load defaults only once ?!

    if mode_check_get not in ["check", "get"]:
        mode_check_get = "check"

    try:
        defaults: list[str] = _load_yml(cfg_defaults_fn, cfg_path)[cfg_keyname]

        if cfg_value_to_search:
            values_exists = defaults.__contains__(cfg_value_to_search)
            if mode_check_get == "check":
                return values_exists
            elif values_exists:
                return defaults[cfg_value_to_search]
        else:
            return defaults

    except TypeError as e:
        return e
    except AttributeError as e:
        return e
    except Exception as e:
        return e


def _load_yml(cfg_filename: str = "defaults", cfg_path: str = "config") -> dict:
    """
    Loads a YAML from 'root/[cfg_path]/[cfg_filename].yml', parses and returns it
    """

    # sanitize
    # TODO case-insensitive yml and yaml as RegExp on end of str
    if ".yml" in cfg_filename:
        cfg_filename = cfg_filename.replace(".yml", "")
    cfg_path = _sanitize_path(cfg_path)

    # create absolute path
    cfg_abs_path = split(dirname(abspath(__file__)))[0]
    cfg_abs_path = join(cfg_abs_path, cfg_path, f"{cfg_filename}.yml")

    if debug_on_glob:
        debug(f"load: {cfg_abs_path}")

    if not exists(cfg_abs_path):
        return FileNotFoundError

    try:
        with open(cfg_abs_path, encoding="utf8") as yml:
            return safe_load(yml)
    except Exception as e:
        error(e)
        return e
