#!/usr/bin/env python
"""
Download and save components from providers, e.g. Hugging Face.
Components could be models, datasets, tokenizers, metrics etc.
"""
# TODO function def with actual objects, not placeholder 'object'
from os import environ

from datasets import list_datasets, list_metrics, load_dataset, load_metric
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def prepare_ml_components(
    dataset: dict,
    model_full_name: str,
    metrics_to_load: list,
    provider: str,
    providerobj: dict,
) -> list:
    """ """
    get_tokenized_dataset(get_dataset(dataset), get_tokenizer(model_full_name))
    get_model(model_full_name, dataset["num_labels"])
    if provider == "wandb":
        set_wandb_env(providerobj)

    return get_metrics(metrics_to_load)


def get_tokenizer(model_full_name: str) -> AutoTokenizer:  # TODO check return type
    """
    Downloads tokenizer specified by model
    """
    AutoTokenizer.from_pretrained(
        model_full_name, use_fast=True, truncation=True, padding=True
    )


def get_model(
    model_full_name: str, num_labels: int
) -> AutoModelForSequenceClassification:  # TODO check return type
    """
    Downloads specified model
    """
    AutoModelForSequenceClassification.from_pretrained(
        model_full_name, num_labels=num_labels
    )


def _get_tokenized_dataset(dataset: object, tokenizer: object) -> object:
    """
    Loads dataset, splits into train/eval/test and tokenizes
    """
    # tokenize
    dataset_tokenized = dataset.map(
        tokenize_dataset(dataset, dataset["colstokens"], tokenizer), batched=True
    )

    # remove columns not neccessary
    try:
        dataset_tokenized = dataset_tokenized.remove_columns(
            dataset["colstokens"]
        ).remove_columns(dataset["colsremove"])
    except Exception as e:
        return e

    return dataset_tokenized


def _get_dataset(dataset: dict) -> object:

    try:
        if dataset["configuration"] == "":
            # print(f'Downloading "{dataset['configuration']}"')
            dataset_plain = load_dataset(dataset["configuration"])
        else:
            # print(f'Downloading "{dataset['configuration']}" from "{dataset['name']}"')
            dataset_plain = load_dataset(dataset["name"], dataset["configuration"])
    except Exception as e:
        return e

    # get unique labels and save into dataset-object
    dataset["num_labels"] = len(dataset_plain["train"].unique(dataset["colsrename"]))

    # rename column 'dscol_rename', model expects 'labels'
    # loop through train/eval/test
    # TODO catch or elif if coumns not contained in dataset?
    for name in dataset_plain:
        if dataset["colsrename"] in dataset_plain[name].column_names:
            dataset_plain[name] = dataset_plain[name].rename_column(
                dataset["colsrename"], "labels"
            )
        # else:
        #     msg = dataset['colsrename']
        #     msg = f'Attribute/Feature/Column "{msg}" not found in "{name}"'
        #     msg += f'\nFound: {dataset_plain[name].column_names}'

    return dataset_plain


def _tokenize_dataset(
    dataset: object, ds_colstokens: list, tokenizer: object
) -> object:
    """
    Returns tokenized dataset
    """
    # TODO use lambda or list comprehension with tupels instead of explicit elif
    colen = len(ds_colstokens)
    # TODO use cached tokenizer
    tokenizer = -1
    try:
        if colen == 3:
            return tokenizer(
                dataset[ds_colstokens[0]],
                dataset[ds_colstokens[1]],
                dataset[ds_colstokens[2]],
                truncation=True,
            )
        elif colen == 2:
            return tokenizer(
                dataset[ds_colstokens[0]], dataset[ds_colstokens[1]], truncation=True
            )
        elif colen == 1:
            return tokenizer(dataset[ds_colstokens[0]], truncation=True)
    except Exception as e:
        return e


def _get_metrics(metrics_to_load: list) -> list:

    metrics_loaded = []

    # downloading metrics builder scripts
    try:
        for met in metrics_to_load:
            print(f'Downloading builder script for "{met}"')
            metrics_loaded.append(load_metric(met))
    except Exception as e:
        return e

    return metrics_loaded


def _set_wandb_env(wandb_param: dict) -> int:
    # TODO set without return, test if dict is valid
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


# def _set_storage():
# TODO implement if needed, maybe use PVC ?
#     #from google.colab import drive
#     return -1
