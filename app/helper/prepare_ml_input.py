#!/usr/bin/env python
"""
Download and save components from providers, e.g. Hugging Face.
Components could be models, datasets, tokenizers, metrics etc.
"""
# TODO function def with actual objects, not placeholder 'object'
from logging import debug
from os import environ

from datasets import load_dataset, load_metric
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def prepare_ml_components(
    dataset: dict, model_full_name: str, providerobj: dict
) -> None:
    """Tokenize dataset and load model"""

    try:
        _get_tokenized_dataset(_get_dataset(dataset), _get_tokenizer(model_full_name))
        _get_model(model_full_name, dataset["num_labels"])
        _set_provider_env(providerobj)
    except Exception as e:
        return e


def get_metrics_to_load_objects(metrics_to_load: list) -> list[dict]:
    """TODO"""

    return _get_metrics(metrics_to_load)


def _get_tokenizer(model_full_name: str) -> AutoTokenizer:  # TODO check return type
    """
    Downloads tokenizer specified by model
    """

    debug(f"Downloading Tokenizer for {model_full_name=}")
    AutoTokenizer.from_pretrained(
        model_full_name, use_fast=True, truncation=True, padding=True
    )


def _get_model(
    model_full_name: str, num_labels: int
) -> AutoModelForSequenceClassification:  # TODO check return type
    """
    Downloads specified model
    """

    debug(f"Downloading {model_full_name=} with {num_labels=}")
    AutoModelForSequenceClassification.from_pretrained(
        model_full_name, num_labels=num_labels
    )


def _get_dataset(dataset: dict) -> object:
    """TODO"""

    ds_name, ds_config = [dataset["dataset"], dataset["configuration"]]

    try:
        if ds_config:
            debug(f"Downloading configuration {ds_config=} from dataset {ds_name=}")
            dataset_plain = load_dataset(ds_name, ds_config)
        else:
            debug(f"Downloading dataset {ds_name=}")
            dataset_plain = load_dataset(ds_name)
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


def _get_tokenized_dataset(dataset: object, tokenizer: object) -> object:
    """
    Loads dataset, splits into train/eval/test and tokenizes
    """

    # tokenize
    dataset_tokenized = dataset.map(
        _tokenize_dataset(dataset, dataset["colstokens"], tokenizer), batched=True
    )

    # remove columns not neccessary
    try:
        dataset_tokenized = dataset_tokenized.remove_columns(
            dataset["colstokens"]
        ).remove_columns(dataset["colsremove"])
    except Exception as e:
        return e

    return dataset_tokenized


def _tokenize_dataset(
    dataset: object, ds_colstokens: list, tokenizer: object
) -> object:
    """
    Returns tokenized dataset
    """

    # TODO use lambda or list comprehension with tupels instead of explicit elif
    colen = len(ds_colstokens)
    # TODO use cached tokenizer
    # tokenizer = -1
    debug("Tokenizing dataset")
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


def _get_metrics(metrics_to_load: list) -> list[dict]:

    metrics_loaded = []

    # downloading metrics builder scripts
    try:
        for met in metrics_to_load:
            print(f'Downloading builder script for "{met}"')
            metrics_loaded.append(load_metric(met))
    except Exception as e:
        return e

    return metrics_loaded


def _set_provider_env(wandb_param: dict) -> None:
    """"""

    try:
        for k, v in wandb_param.items():
            environ[k] = v
    except Exception as e:
        return e
