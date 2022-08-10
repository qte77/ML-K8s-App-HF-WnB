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

from datasets import dataset_dict
from transformers import AutoTokenizer

from .load_hf_components import (
    get_dataset,
    get_metrics_to_load_objects_hf,
    get_model,
    get_tokenizer,
    set_debug_state_hf,
)


def set_debug_state(debug_on: bool = False):
    global debug_state
    debug_state = debug_on
    set_debug_state_hf(debug_on)


def prepare_ml_components(dataset: dict, model_full_name: str) -> str:
    """Load tokenized dataset and model"""

    try:
        dataset_plain = get_dataset(dataset["dataset"], dataset["configuration"])

        # TODO get dataset card and extract num_labels instead of count
        dataset["num_labels"] = len(
            dataset_plain["train"].unique(dataset["col_to_rename"])
        )

        _ = _get_tokenized_dataset(
            dataset_plain,
            get_tokenizer(model_full_name),
            dataset["cols_to_tok"],
            dataset["cols_to_remove"],
        )
        _ = get_model(model_full_name, dataset["num_labels"])

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
    """
    Downloads metrics objects by calling the appropriate handling function.
    To date onyl from Hugging Face
    """
    return get_metrics_to_load_objects_hf(metrics_to_load)


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
