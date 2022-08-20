#!/usr/bin/env python
"""Load configuration files"""

from os import environ as env
from os.path import join
from typing import Final, Literal, Optional, Union

from omegaconf import OmegaConf

if "APP_DEBUG_IS_ON" in env:
    from logging import debug

    global debug_on_global
    debug_on_global: Final = True

from .check_sanitize_path import sanitize_path


def load_defaults(
    cfg_defaults_fn: str = "defaults", cfg_path: str = "app/config"
) -> None:
    """
    Load the defaults from '<cfg_defaults_fn>' and creates
    a global copy inside the module
    """

    global default_configs
    default_configs = _load_config(cfg_defaults_fn, cfg_path)

    if debug_on_global:
        debug(f"{default_configs=}")


def get_defaults(key_to_search_and_return: str = "save_dir") -> str:
    """
    Searches for '<key_to_search_and_return>' inside 'defaults.yml'
    and returns its value if found
    """
    return default_configs[key_to_search_and_return]


def get_config_content(
    cfg_filename_ex_ext: str = "defaults", cfg_path: str = "app/config"
) -> dict:
    """Returns config objects"""

    if debug_on_global:
        defaults_dbg_msg = f"'{cfg_filename_ex_ext}' found in defaults."
        if _check_or_get_default("config_fn", cfg_filename_ex_ext):
            debug(defaults_dbg_msg)
        else:
            debug(f"No {defaults_dbg_msg} Trying to find the file anyway.")

    return _load_config(cfg_filename_ex_ext, cfg_path)


def get_keyfile_content(provider: str = "wandb") -> dict:
    """Returns keyfile objects"""

    try:
        # TODO handle multiple keyfiles
        keyfile_default = "~/wandb.key.yml" if provider == "wandb" else "~/key.yml"
        keyfiles = default_configs.get("keyfiles", keyfile_default)
        keyfile = sanitize_path(keyfiles[provider])

        if debug_on_global:
            debug(f"{keyfile=}")

        # TODO refactor to less convoluted call
        return _load_config(keyfile["base"], keyfile["dir"])
    except Exception as e:
        return e


def _load_config(
    cfg_filename_ex_ext: str = "defaults", cfg_path: str = "app/config"
) -> dict:
    """Loads and returns a config. Only accepts yml."""

    if debug_on_global:
        debug(f"Loading {cfg_filename_ex_ext=}")
    try:
        # TODO sanitization of yml extension.
        config = OmegaConf.load(join(cfg_path, f"{cfg_filename_ex_ext}.yml"))
        return OmegaConf.to_object(config)
    except Exception as e:
        return e


def _check_or_get_default(
    cfg_value_to_search: str = None,
    mode_check_get: Optional[Literal["check", "get"]] = "check",
) -> Union[bool, str]:
    """Checks whether a default exists or returns it if 'get' is provided"""

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
