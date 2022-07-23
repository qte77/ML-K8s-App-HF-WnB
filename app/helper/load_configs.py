#!/usr/bin/env python
"""Load configuration files"""
from os.path import exists
from yaml import safe_load

#TODO export config in files.yml to separate from program flow?
cfg_path = "../config"
cfg_defaults = [ 
    'defaults' 'task',
    'huggingface', 'wandb',
    'sweep', 'sweep-wandb'
]

def get_config(cfg_name: str) -> object:
    """Parses config yaml and returns config objects"""
    if cfg_defaults.__contains__(cfg_name):
        cfg = cfg_defaults[cfg_name]
    else:
        cfg = cfg_name

    cfg = f'{cfg_path}/{cfg}.yml'

    if not exists(cfg):
        return FileNotFoundError

    try:
        with open(cfg, 'r', encoding='utf8') as yml:
            return safe_load(yml)
    except Exception as e:
        return e