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

from datasets import dataset_dict, load_dataset, load_metric
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def set_debug_state(debug_on: bool = False):
    global debug_state
    debug_state = debug_on


def prepare_ml_components(dataset: dict, model_full_name: str) -> str:
    """Load tokenized dataset and model"""

    try:
        dataset_plain = _get_dataset(dataset["dataset"], dataset["configuration"])
        dataset["num_labels"] = len(
            dataset_plain["train"].unique(dataset["col_to_rename"])
        )
        tokenizer = _get_tokenizer(model_full_name)
        _ = _get_tokenized_dataset(
            dataset_plain,
            tokenizer,
            dataset["cols_to_tok"],
            dataset["cols_to_remove"],
        )
        _ = _get_model(model_full_name, dataset["num_labels"])
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


def _get_model(
    model_full_name: str, num_labels: int
) -> AutoModelForSequenceClassification:  # TODO check return type
    """Downloads specified model"""

    if debug_state:
        debug(f"Downloading {model_full_name=} with {num_labels=}")
    return AutoModelForSequenceClassification.from_pretrained(
        model_full_name, num_labels=num_labels
    )


def _get_dataset(dataset: str, configuration: str) -> dataset_dict.DatasetDict:
    """TODO"""

    try:
        if configuration:
            if debug_state:
                debug(f"Downloading {configuration=} from {dataset=}")
            return load_dataset(dataset, configuration)
        else:
            if debug_state:
                debug(f"Downloading dataset {dataset=}")
            return load_dataset(dataset)
    except Exception as e:
        return e


def get_metrics_to_load_objects(metrics_to_load: list) -> list[dict]:
    """Downloads Hugging Face Metrics Builder Scripts"""

    if debug_state:
        debug(f"Loading HF Metrics Builder Scripts for {metrics_to_load}")

    try:
        return [load_metric(met) for met in metrics_to_load]
    except Exception as e:
        return e


def _get_tokenizer(model_full_name: str) -> AutoTokenizer:  # TODO check return type
    """Downloads tokenizer for the specified model"""

    if debug_state:
        debug(f"Downloading Tokenizer for {model_full_name=}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_full_name, use_fast=True, truncation=True, padding=True
    )

    if debug_state:
        tok_msg = "This is a test sentence."
        tok_res = tokenizer.encode(tok_msg)
        debug(f"Tokenizing '{tok_msg}': {tok_res}")

    return tokenizer


def _get_raw_tokenized_dataset(
    dataset_plain: dataset_dict.DatasetDict, tokenizer: object, cols_to_tok: list[str]
) -> dataset_dict.DatasetDict:
    """Returns tokenized dataset"""

    def _tokenize(ds):
        cols = [ds[col] for col in cols_to_tok]
        return tokenizer(*cols, truncation=True)

    return dataset_plain.map(_tokenize, batched=True)


def _get_tokenized_dataset(
    dataset_plain: dataset_dict.DatasetDict,
    tokenizer: AutoTokenizer,
    cols_to_tok: list[str],
    cols_to_remove: list[str],
) -> dataset_dict.DatasetDict:
    """TODO"""
    # TODO save local copy of dataset_tokenized

    if debug_state:
        debug(f"Tokenizing dataset with {len(cols_to_tok)} columns to tokenize and")
        debug(f"Removing {cols_to_tok=} and {cols_to_remove=} from tokenized dataset")

    try:
        return (
            _get_raw_tokenized_dataset(dataset_plain, tokenizer, cols_to_tok)
            .remove_columns(cols_to_tok)
            .remove_columns(cols_to_remove)
        )
    except Exception as e:
        return e
