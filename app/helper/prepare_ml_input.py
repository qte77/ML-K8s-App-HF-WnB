#!/usr/bin/env python
"""
Download and save components from providers, e.g. Hugging Face.
Components could be models, datasets, tokenizers, metrics etc.
"""

# TODO return None or Exception ?
# TODO load local versions of models, datasets, metrics and tokenizer if not cached
# TODO function def with actual objects, not placeholder 'object'
from logging import debug
from os import environ
from typing import Union

from datasets import dataset_dict, load_dataset, load_metric
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def set_debug_state(debug_on: bool = False):
    global debug_state
    debug_state = debug_on


def prepare_ml_components(dataset: dict, model_full_name: str) -> str:
    """Load tokenized dataset and model"""

    try:
        dataset["num_labels"] = _get_tokenized_dataset(dataset, model_full_name)
        _get_model(model_full_name, dataset["num_labels"])
    except Exception as e:
        return e


def set_provider_env(provider: str, provider_param: dict) -> None:
    """Set the environment parameters for the sweep provider"""

    try:
        for k, v in provider_param.items():
            environ[k] = v
            if debug_state:
                debug(f"Setting '{provider}' env '{k}'")
    except Exception as e:
        return e


def get_metrics_to_load_objects(metrics_to_load: list) -> list[dict]:
    """Downloads Hugging Face Metrics Builder Scripts"""

    # metrics_loaded = []
    if debug_state:
        debug(f"Loading HF Metrics Builder Scripts for {metrics_to_load}")

    try:
        # for met in metrics_to_load:
        #     if debug_state:
        #         debug(f"Downloading HF Metrics Builder Script for '{met}'")
        #     metrics_loaded.append(load_metric(met))
        # return metrics_loaded
        return [load_metric(met) for met in metrics_to_load]
    except Exception as e:
        return e


def _get_tokenizer(model_full_name: str) -> AutoTokenizer:  # TODO check return type
    """
    Downloads tokenizer specified by model
    """

    if debug_state:
        debug(f"Downloading Tokenizer for {model_full_name=}")

    return AutoTokenizer.from_pretrained(
        model_full_name, use_fast=True, truncation=True, padding=True
    )


def _get_model(
    model_full_name: str, num_labels: int
) -> AutoModelForSequenceClassification:  # TODO check return type
    """
    Downloads specified model
    """

    if debug_state:
        debug(f"Downloading {model_full_name=} with {num_labels=}")
    AutoModelForSequenceClassification.from_pretrained(
        model_full_name, num_labels=num_labels
    )


def _get_dataset(dataset: dict) -> Union[dataset_dict.DatasetDict, str]:
    """TODO"""

    ds_name, ds_config = [dataset["dataset"], dataset["configuration"]]

    try:
        if ds_config:
            if debug_state:
                debug(f"Downloading configuration {ds_config=} from dataset {ds_name=}")
            dataset_plain = load_dataset(ds_name, ds_config)
        else:
            if debug_state:
                debug(f"Downloading dataset {ds_name=}")
            dataset_plain = load_dataset(ds_name)
    except Exception as e:
        return e

    # get unique labels and save into dataset-object
    num_labels = len(dataset_plain["train"].unique(dataset["col_to_rename"]))

    # rename column '[col_to_rename]' bceause model expects 'labels'
    # loop through train/eval/test
    # TODO catch or elif if coumns not contained in dataset?
    for name in dataset_plain:
        if dataset["col_to_rename"] in dataset_plain[name].column_names:
            dataset_plain[name] = dataset_plain[name].rename_column(
                dataset["col_to_rename"], "labels"
            )
        else:
            msg = dataset["col_to_rename"]
            msg = f"Attribute/Feature/Column '{msg}' not found in '{name}'"
            if debug_state:
                debug(f"{msg}\nFound: {dataset_plain[name].column_names}")

    # TODO save local copy of dataset_plain

    return dataset_plain, num_labels


def _tokenize_dataset(
    dataset_plain: object, cols_to_tok: list[str], tokenizer: object
) -> object:
    """Returns tokenized dataset"""

    if debug_state:
        debug(f"Tokenizing dataset with {len(cols_to_tok)} columns to tokenize")

    def _tokenize(dataset_plain):
        cols = [dataset_plain[col] for col in cols_to_tok]
        return tokenizer(*cols, truncation=True)

    return dataset_plain.map(_tokenize, batched=True)


def _remove_columns_from_dataset(
    dataset_tokenized: dataset_dict.DatasetDict,
    cols_to_tok: list[str],
    cols_to_remove: list[str],
):
    """Remove columns from dataset"""

    if debug_state:
        debug(f"Removing columns {cols_to_tok} and {cols_to_remove}")

    try:
        return dataset_tokenized.remove_columns(cols_to_tok).remove_columns(
            cols_to_remove
        )
    except Exception as e:
        return e


def _get_tokenized_dataset(dataset: str, model_full_name: str) -> str:
    """
    Loads dataset, splits into train/eval/test and tokenizes
    """
    # TODO save local copy of dataset_tokenized

    dataset_plain, num_labels = _get_dataset(dataset)
    tokenizer = _get_tokenizer(model_full_name)
    dataset_tokenized = _tokenize_dataset(
        dataset_plain, dataset["cols_to_tok"], tokenizer
    )
    dataset_tokenized = _remove_columns_from_dataset(
        dataset_tokenized, dataset["cols_to_tok"], dataset["cols_to_remove"]
    )

    if debug_state:
        tok_msg = "This is a test sentence."
        tok_res = tokenizer.encode(tok_msg)
        debug(f"Tokenizing '{tok_msg}': {tok_res}")

    return num_labels
