#!/usr/bin/env python
'''
Train model
'''
from ..helper.prepare_sweep import start_sweep
from transformers import Trainer, TrainingArguments, Metric
#import bert_score
from wandb import log
from numpy import argmax


def train_model(
  project_name: str,
  metric_to_optimize: str,
  metrics_loaded: list,
  sweep_config: dict,
  provider: str
) -> object:

  start_sweep(provider)

  return NotImplementedError


def _compute_metrics(
  eval_pred: list, #TOCO check type
  metrics_loaded: list,
  metrics_avg: str
) -> Metric:

  #TODO refactor 
  predictions, labels = eval_pred
  predictions = argmax(predictions, axis = 1) #predictions.argmax(-1)
  
  print("*************")
  
  for i, m in enumerate(metrics_loaded):

    if metrics_loaded[i] in ['precision','recall','f1']:
      met = m.compute(
        predictions = predictions,
        references = labels,
        average = metrics_avg
      )
    else:
      met = m.compute(
        predictions = predictions,
        references = labels
      )

    if metrics_loaded[i] == 'accuracy':
      ret = met

    log(met)
    print(met)
    
  print("*************")

  return ret


def _create_trainer(config = None) -> Trainer:
  #TODO implement
  #TODO save locally

  # config = config.config

  # # Initialize a new wandb run
  # with wandb.init(config = config):
  #   # If called by wandb.agent, as below,
  #   # this config will be set by Sweep Controller
  #   config = wandb.config

  #   eval_steps = round(config.max_steps / 5)
  #   save_steps = eval_steps * 2

  #   # args need to be assigned here to avoid wandb runtime TypeError()
  #   # "'TrainingArguments' object does not support item assignment"
  #   args = transformers.TrainingArguments(
  #     report_to = 'wandb',
  #     output_dir = os.environ['WANDB_PROJECT'],
  #     overwrite_output_dir = True,
  #     # check evaluation metrics at each epoch
  #     evaluation_strategy = 'steps',
  #     logging_steps = 100,
  #     load_best_model_at_end = True,
  #     run_name = os.environ['WANDB_PROJECT'],
  #     eval_steps = eval_steps,
  #     save_steps = save_steps,
  #     metric_for_best_model = metric_to_optimize,
  #     greater_is_better = greaterBool,
  #     # avoid info 'The following columns in the evaluation set  don't have a corresponding argument'
  #     # remove_unused_columns = True,
  #     # the following will be changed by sweep agent
  #     learning_rate = config.learning_rate,
  #     max_steps = config.max_steps,
  #     seed = config.seed,
  #     optim = config.optim
  #   )

    # trainer = transformers.Trainer(
    #   model = modelobj,
    #   args = args, 
    #   train_dataset = dataset_tokenized['train'],
    #   eval_dataset = dataset_tokenized['test'],
    #   tokenizer = tokenizer,
    #   compute_metrics = compute_metrics #()
    # )

  #   print(orange,"*************")
  #   print("Metric: %s, #Labels: %s, Avg: %s" % (metric_to_optimize, num_labels, ds_avg))
  #   print("eval_steps: %s, save_steps: %s" % (eval_steps, save_steps))
  #   print(orange,"*************")

  # return trainer
  
  return NotImplementedError