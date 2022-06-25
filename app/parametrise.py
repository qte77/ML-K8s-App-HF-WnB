#!/usr/bin/env python
'''
Returns parameter object
'''
#TODO rename 'defaults' more specific and descriptive
#TODO generalize provider parametrisation
import loadcfg
import os
from torch import device
from torch.cuda import is_available

def get_param_object():

  defaults = loadcfg.get_config('defaults')
  hf_params = loadcfg.get_config('huggingface')
  sweep = loadcfg.get_config('sweep')
  task = loadcfg.get_config('task')

  paramobj = {}
  paramobj['sweep'] = get_sweep_cfg(sweep)
  paramobj['device'] = get_device()
  paramobj['dataset'] = get_dataset_cfg(hf_params['datasets'], task['dataset'])
  paramobj['project_name'] = get_project_name(
    task['model'], paramobj['dataset']['name'],
    paramobj['device'], paramobj['sweep']['is_sweep']
  )
  if paramobj['sweep']['is_sweep']:  
    #TODO case
    if paramobj['sweep']['provider'] == 'wandb':
      wandb_params = loadcfg.get_config('wandb')
      paramobj['wandb'] = get_wandb_env(
        wandb_params, paramobj['project_name']
      )
  paramobj['defaults'] = get_defaults(defaults)
  paramobj['model_full_name'] = get_model_full_name(hf_params['models'], task['model'])
  paramobj['metrics']['metric_to_optimize'] = get_metric_to_optimize_cfg(
    hf_params['metrics_to_optimize'], task['metric_to_optimize']
  )
  paramobj['metrics']['metrics_to_load'] = get_metrics_to_load(
    hf_params['metrics_secondary_possible'] ,task['metrics_to_load']
  )

  return paramobj

def get_defaults(defaults):

  if not defaults.save_dir == '':
    return { 'save_dir' : defaults.save_dir }
  else:
    return { 'save_dir' : './data' }

def get_dataset_cfg(datasets, dataset):

  datasetobj = {}
  try:
    dataset = dataset.lower()
    datasetobj['name'], datasetobj['configuration'], datasetobj['avg'], \
      datasetobj['colsrename'], datasetobj['colstokens'], \
      datasetobj['colsremove'] = datasets.get(
        dataset, ['Invalid dataset', '']
      )
    return datasetobj
  except Exception as e:
    return e
  
def get_model_full_name(models, model):

  try:
    model = model.lower()
    return models.get(
      model, ['Invalid model', '']
    )
  except Exception as e:
    return e

def get_metric_to_optimize_cfg(metrics_to_optimize, metric_to_optimize):

  metricobj = {}
  try:
    metric_to_optimize = metric_to_optimize.lower()
    metricobj['goal'], metricobj['greater_is_better'] = \
      metrics_to_optimize.get(
        metric_to_optimize, ['Invalid metric', '']
      )
    return metricobj
  except Exception as e:
    return e

def get_metrics_to_load(metrics_secondary_possible, metrics_to_load):
  
  metrics = []
  try:
    for metric in metrics_to_load:
      metrics.append() if metrics_secondary_possible.count(metric) else print(f"{metric} not contained")
    return metrics
  except Exception as e:
    return e

def get_device():
  
  try:
    os.environ['TPU_NAME']
    return 'tpu'
  except:
    try:
      return device('cuda' if is_available() else 'cpu')
    except Exception as e:
      return e

def get_project_name(model, dataset_name, device, is_sweep):

  suffix = '-sweep' if is_sweep else ''
  try:
    return f'{model}-{dataset_name}-{device}{suffix}'
  except Exception as e:
    return e

def get_wandb_env(wandb_params, project_name):
  '''
  Checks for API-key first. Returns exception if not found
  Expects keyfile as yaml:
    username: ''
    key: ''
  '''
  try:
    wandb_user_key = loadcfg.get_config(wandb_params['wandb_keyfile'])
  except Exception as e:
    return e('API-key not found')

  wandbobj = {}
  wandbobj['username'] = wandb_user_key['username']
  wandbobj['key'] = wandb_user_key['key']
  wandbobj['entity'] = wandb_params['entity']
  wandbobj['project'] = project_name
  wandbobj['watch'] = wandb_params['watch']
  wandbobj['save_code'] = wandb_params['save_code']
  wandbobj['log_model'] = wandb_params['log_model']
  
  return wandbobj

def get_sweep_cfg(sweep):

  sweepobj = {}
  sweepobj['is_sweep'] = True if sweep.train_count > 1 else False
  if sweepobj['is_sweep']:
    sweepobj['train_count'] = sweep.train_count
    sweepobj['provider'] = sweep.provider
    sweepobj['config'] = loadcfg(f'sweep-{sweep.provider}')

  return sweepobj
