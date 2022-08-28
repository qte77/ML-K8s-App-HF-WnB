#!/usr/bin/env python
"""Offers functions to handle sweeps"""
# from wandb import agent, login, sweep
# from ..utils.configure_logging import debug_on_global

# from logging import getLogger
#
# logger = getLogger(__name__)


def _login_to_provider(provider: str) -> None:
    """Trys to login to provider with API key"""

    # TODO incorp --cloud and $WANDB_KEY into login-fun
    # login()

    return NotImplementedError


def _create_sweep(sweep_config: dict, project_name: str) -> str:
    """
    Creates wandb sweep and returns sweep id provided by wandb controller
    """

    # if env WANDB_ENTITY not used: entity=<entity>
    # return sweep(sweep_config.config, project=project_name)

    return NotImplementedError


def start_sweep(provider: str) -> None:
    """TODO"""

    # _login_to_provider(provider)
    # _create_sweep()

    # if env WANDB_ENTITY not used: entity=<entity>
    # agent(
    #     _create_sweep(sweep_config.config, project_name),
    #     _create_trainer(metric_to_optimize, metrics_loaded),
    #     count=sweep_config["train_count"],
    # )

    return NotImplementedError
