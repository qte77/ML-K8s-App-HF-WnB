#!/usr/bin/env python
'''
Download and save components from Hugging Face
'''
import os
from datasets import load_dataset, list_datasets, list_metrics, load_metric
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def prepare(dataset, model_full_name, metrics_to_load, sweep, wandb):

    get_tokenizer(model_full_name)
    get_tokenized_dataset(dataset)
    get_model(model_full_name, dataset['num_labels'])
    if sweep['provider'] == 'wandb':
        set_wandb_env(wandb)

    return get_metrics(metrics_to_load)

def get_tokenized_dataset(dataset, tokenizer):
    '''
    Loads dataset, splits into train/eval/test and tokenizes
    '''
    #tokenize
    dataset_tokenized = dataset.map(
        tokenize_dataset(
            get_dataset(dataset),
            dataset['colstokens'],
            tokenizer
        ),
        batched=True
    )

    #remove columns not neccessary
    try:
        dataset_tokenized = dataset_tokenized.remove_columns(
            dataset['colstokens']
        ).remove_columns(
            dataset['colsremove']
        )
    except Exception as e:
        return e

    return dataset_tokenized

def get_dataset(dataset):

    try:
        if dataset['configuration'] == '':
            # print(f'Downloading "{dataset['configuration']}"')
            dataset_plain = load_dataset(dataset['configuration'])
        else:
            # print(f'Downloading "{dataset['configuration']}" from "{dataset['name']}"')
            dataset_plain = load_dataset(dataset['name'], dataset['configuration'])
    except Exception as e:
        return e

    #get unique labels and save into dataset-object
    dataset['num_labels'] = len(dataset_plain['train'].unique(dataset['colsrename']))

    #rename column 'dscol_rename', model expects 'labels'
    #loop through train/eval/test
    #TODO catch or elif if coumns not contained in dataset?
    for name in dataset_plain:
        if dataset['colsrename'] in dataset_plain[name].column_names:
            dataset_plain[name] = dataset_plain[name].rename_column(
                dataset['colsrename'], 'labels'
            )
        # else:
        #     msg = dataset['colsrename']
        #     msg = f'Attribute/Feature/Column "{msg}" not found in "{name}"'
        #     msg += f'\nFound: {dataset_plain[name].column_names}'

    return dataset_plain

def tokenize_dataset(dataset, ds_colstokens):
    #TODO use lambda or function with tupels instead of explicit elif
    colen = len(ds_colstokens)
    #TODO use cached tokenizer
    tokenizer = -1
    try:
        if colen == 3:
            return tokenizer(
                dataset[ds_colstokens[0]],
                dataset[ds_colstokens[1]],
                dataset[ds_colstokens[2]],
                truncation=True
            )
        elif colen == 2:
            return tokenizer(
                dataset[ds_colstokens[0]],
                dataset[ds_colstokens[1]],
                truncation = True
            )
        elif colen == 1:
            return tokenizer(
                dataset[ds_colstokens[0]],
                truncation = True
            )
    except Exception as e:
        return e

def get_tokenizer(model_full_name: str):

    AutoTokenizer.from_pretrained(
        model_full_name,
        use_fast = True,
        truncation = True,
        padding = True
    )

def get_model(model_full_name: str, num_labels: int):
    
    AutoModelForSequenceClassification.from_pretrained(
        model_full_name,
        num_labels = num_labels
    )

def get_metrics(metrics_to_load):
    
    metrics_loaded = []

    #downloading metrics builder scripts
    try:
        for met in metrics_to_load:
            print(f'Downloading builder script for "{met}"')
            metrics_loaded.append(load_metric(met))
    except Exception as e:
        print(e)
        #return e

    return metrics_loaded

def set_wandb_env(wandb_param):

    try:
        os.environ["WANDB_ENTITY"] = wandb_param.entity
        os.environ["WANDB_PROJECT"] = wandb_param.project
        os.environ["WANDB_WATCH"] = wandb_param.watch
        os.environ["WANDB_SAVE_CODE"] = wandb_param.save_code
        os.environ["WANDB_LOG_MODEL"] = wandb_param.log_model
        os.environ["WANDB_LOG_MODEL"] = wandb_param.log_model
        return 0
    except Exception as e:
        return e

def set_storage():
    #TODO
    #from google.colab import drive
    return -1
