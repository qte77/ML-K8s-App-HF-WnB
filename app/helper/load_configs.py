#!/usr/bin/env python
"""Load configuration files"""

from os import environ as env
from os.path import expanduser, join  # , abspath, dirname, exists, split
from typing import Literal, Optional, Union

if "APP_DEBUG_IS_ON" in env:
    from logging import debug

from omegaconf import OmegaConf


def load_defaults(
    cfg_defaults_fn: str = "defaults", cfg_path: str = "app/config"
) -> None:
    """TODO"""

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


def get_default_save_dir() -> dict:
    """Looks for 'save_dir' inside 'defaults.yml' and returns it if found"""
    return default_configs["save_dir"]


def get_keyfile_content(provider: str = "wandb") -> dict:
    """Returns keyfile objects"""
    try:
        # TODO handle multiple keyfiles
        keyfile_default = "~/wandb.key.yml" if provider == "wandb" else "~/key.yml"
        keyfiles = default_configs.get("keyfiles", keyfile_default)
        keyfile = _sanitize_path(keyfiles[provider])

        if "APP_DEBUG_IS_ON" in env:
            debug(f"{keyfile=}")

        # TODO refactor to less convoluted call
        return _load_config(keyfile[-1].replace(".yml", ""), *keyfile[:-1])
    except Exception as e:
        return e


def _load_config(
    cfg_filename_ex_ext: str = "defaults", cfg_path: str = "app/config"
) -> dict:
    """Loads and returns a config. Only accepts yaml/yml."""
    if "APP_DEBUG_IS_ON" in env:
        debug(f"Loading {cfg_filename_ex_ext=}")
    try:
        # TODO sanitization of yaml/yml extension
        config = OmegaConf.load(join(cfg_path, f"{cfg_filename_ex_ext}.yml"))
        return OmegaConf.to_object(config)
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


def _sanitize_path(path: str = "~") -> list[str]:
    """Expands '~' to $HOME if given and returns OS-specific path"""

    try:
        if "\\" in path:
            path = path.replace("\\", "/")
        if path.startswith("~"):
            path = expanduser(path)
        return path.split("/")
    except Exception as e:
        return e
