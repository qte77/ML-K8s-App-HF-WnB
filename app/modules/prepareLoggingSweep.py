#!/usr/bin/env python
'''
Train model
'''
from wandb import login, init, sweep, agent


def login_to_provider(provider: str) -> None:
    
    #TODO incorp --cloud and $WANDB_KEY into login-fun
    wandb.login()


def create_sweep(
    sweep_config: dict,
    project_name: str
) -> str:
    '''
    Creates wandb sweep and returns sweep id provided by wandb controller
    '''
    #if env WANDB_ENTITY not used: entity=<entity>
    return wandb.sweep(sweep_config.config, project = project_name)
