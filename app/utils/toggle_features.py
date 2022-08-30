#!/usr/bin/env python
"""
TODO
"""

from .handle_logging import debug_on_global, logging_facility


def toggle_global_pydantic(toggle_pydantic: bool = False):
    """Toggle `global pydantic_on_global` to `toggle_pydantic`"""

    global pydantic_on_global
    pydantic_on_global = toggle_pydantic

    if debug_on_global:
        logging_facility("log", f"{pydantic_on_global=}")
