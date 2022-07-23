#!/usr/bin/env python
"""
Train model
"""
from wandb import login, sweep, agent

def _login_to_provider(provider: str) -> None:

    #TODO incorp --cloud and $WANDB_KEY into login-fun
    login()
    
def _create_sweep(
    sweep_config: dict,
    project_name: str
) -> str:
    """
    Creates wandb sweep and returns sweep id provided by wandb controller
    """
    #if env WANDB_ENTITY not used: entity=<entity>
    return sweep(sweep_config.config, project = project_name)

def start_sweep(
    
) -> None:

    _login_to_provider(provider)

    #if env WANDB_ENTITY not used: entity=<entity>
    agent(
        _create_sweep(sweep_config.config, project_name),
        _create_trainer(metric_to_optimize, metrics_loaded),
        count = sweep_config['train_count']
    )
