#!/usr/bin/env python
"""Load configuration files"""

from os import environ as env
from os.path import join  # , expanduser , abspath, dirname, exists, split
from typing import Literal, Optional, Union

if "APP_DEBUG_IS_ON" in env:
    from logging import debug

from omegaconf import OmegaConf


def load_defaults(
    cfg_defaults_fn: str = "defaults", cfg_path: str = "app/config"
) -> None:
    global default_configs
    default_configs = _load_config(cfg_defaults_fn, cfg_path)
    if "APP_DEBUG_IS_ON" in env:
        debug(f"{default_configs=}")


def get_config_content(
    cfg_filename_ex_ext: str = "defaults", cfg_path: str = "app/config"
) -> dict:
    """Returns config objects"""

    if "APP_DEBUG_IS_ON" in env:
        defaults_dbg_msg = f"'{cfg_filename_ex_ext}' found in defaults."
        if _check_or_get_default("config_fn", cfg_filename_ex_ext):
            debug(defaults_dbg_msg)
        else:
            debug(f"No {defaults_dbg_msg} Trying to find the file anyway.")

    return _load_config(cfg_filename_ex_ext, cfg_path)


def _load_config(
    cfg_filename_ex_ext: str = "defaults", cfg_path: str = "app/config"
) -> OmegaConf:
    """Loads and returns a config. Only accepts yaml/yml."""
    if "APP_DEBUG_IS_ON" in env:
        debug(f"Loading {cfg_filename_ex_ext=}")
    try:
        # TODO sanitization of yaml/yml extension
        config = OmegaConf.load(join(cfg_path, f"{cfg_filename_ex_ext}.yml"))
    except Exception as e:
        return e
    return config


def get_default_save_dir() -> dict:
    """Looks for 'save_dir' inside 'defaults.yml' and returns it if found"""
    return default_configs["save_dir"]


def get_keyfile_content(provider: str = "wandb") -> dict:
    """Returns keyfile objects"""
    try:
        # TODO handle multiple keyfiles
        keyfile_default = "~/wandb.key.yml" if provider == "wandb" else "~/key.yml"
        keyfiles = default_configs.get("keyfiles", keyfile_default)
        return OmegaConf.load(keyfiles)
    except Exception as e:
        return e


def _check_or_get_default(
    cfg_value_to_search: str = None,
    mode_check_get: Optional[Literal["check", "get"]] = "check",
) -> Union[bool, str]:
    """TODO"""

    if mode_check_get not in ["check", "get"]:
        mode_check_get = "check"

    if cfg_value_to_search:
        values_exists = default_configs.__contains__(cfg_value_to_search)
        if mode_check_get == "check":
            return values_exists
        elif values_exists:
            return default_configs[cfg_value_to_search]
        else:
            return ValueError
    else:
        return default_configs


# def _sanitize_path(path: str = "~") -> str:
#     """Expands '~' to $HOME if given and returns OS-specific path"""

#     if "\\" in path:
#         path = path.replace("\\", "/")
#     if path.startswith("~"):
#         path = expanduser(path)

#     return join(*path.split("/"))


# def _load_yml(cfg_filename: str = "defaults", cfg_path: str = "config") -> dict:
#     """
#     Loads a YAML from 'root/[cfg_path]/[cfg_filename].yml', parses and returns it
#     """

#     # sanitize
#     # TODO case-insensitive yml and yaml as RegExp on end of str
#     if ".yml" in cfg_filename:
#         cfg_filename = cfg_filename.replace(".yml", "")
#     cfg_path = _sanitize_path(cfg_path)

#     # create absolute path
#     cfg_abs_path = split(dirname(abspath(__file__)))[0]
#     cfg_abs_path = join(cfg_abs_path, cfg_path, f"{cfg_filename}.yml")

#     if environ["APP_DEBUG_IS_ON"]:
#         debug(f"load: {cfg_abs_path}")

#     if not exists(cfg_abs_path):
#         return FileNotFoundError

#     try:
#         with open(cfg_abs_path, encoding="utf8") as yml:
#             return safe_load(yml)
#     except Exception as e:
#         error(e)
#         return e
