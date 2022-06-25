#!/usr/bin/env python
'''
Train model
TODO implement
'''
from transformers import Trainer, TrainingArguments
#import bert_score
from numpy import argmax
import wandb

# COLOR = {
#   'red' : '\033[31m',
#   'green' : '\033[32m',
#   'orange' : '\033[33m',
#   'endclr' : '\033[0m'
# }

def train(project_name, metric_to_optimize, metrics_loaded, sweep_config):
  #TODO incorp --cloud and $WANDB_KEY into login-fun
  wandb.login() 
  #if env WANDB_ENTITY not used: entity=<entity>
  sweep_id = wandb.sweep(sweep_config.config, project=project_name)
  trainer = get_trainer(metric_to_optimize, metrics_loaded)
  wandb.agent(sweep_id, trainer, count=sweep_config['train_count'])

  return -1

def compute_metrics(eval_pred, metrics_loaded, metrics_avg):
  #TODO
  predictions, labels = eval_pred
  predictions = argmax(predictions, axis = 1) #predictions.argmax(-1)
  
  print("*************")
  
  for i, m in enumerate(metrics_loaded):

    if metrics_loaded[i] in ['precision','recall','f1']:
      met = m.compute(predictions = predictions, references = labels, average = metrics_avg)
    else:
      met = m.compute(predictions = predictions, references = labels)

    if metrics_loaded[i] == 'accuracy':
      ret = met

    wandb.log(met)
    print(met)
    
  print("*************")

  return ret

def get_trainer(config = None):
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
  #   args = TrainingArguments(
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

    # trainer = Trainer(
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
  
  return -1
