#!/usr/bin/env python
"""
Download and save components from providers, e.g. Hugging Face.
Components could be models, datasets, tokenizers, metrics etc.
"""

# TODO return None or Exception ?
# TODO load local versions of models, datasets, metrics and tokenizer if not cached
# TODO function def with actual objects, not placeholder 'object'
from os import environ as env

from datasets import dataset_dict
from transformers import AutoTokenizer

if "APP_DEBUG_IS_ON" in env:
    from logging import debug

from .load_configs import get_keyfile_content
from .load_hf_components import (
    get_dataset_hf,
    get_metrics_to_load_objects_hf,
    get_model_hf,
    get_tokenizer_hf,
)


def prepare_pipeline(paramobj: dict) -> dict:
    """TODO"""

    paramobj["dataset"]["num_labels"] = _get_dataset(
        paramobj["dataset"], paramobj["model_full_name"]
    )
    # paramobj["metrics"]["metrics_loaded"] = _get_metrics_to_load_objects(
    #     paramobj["metrics"]["metrics_to_load"]
    # )
    # _get_model(paramobj["model_full_name"], paramobj["dataset"]["num_labels"])
    # provider = paramobj["sweep"]["provider"]
    # _set_provider_env(provider, paramobj[provider])

    return paramobj


def _get_dataset(dataset: dict, model_full_name: str) -> int:
    """Load tokenized dataset and model"""

    try:
        dataset_plain = get_dataset_hf(dataset["dataset"], dataset["configuration"])

        _ = _get_tokenized_dataset(
            dataset_plain,
            get_tokenizer_hf(model_full_name),
            dataset["cols_to_tok"],
            dataset["cols_to_remove"],
        )

        return len(dataset_plain["train"].unique(dataset["col_to_rename"]))

    except Exception as e:
        return e


def _get_metrics_to_load_objects(metrics_to_load: list) -> list[dict]:
    """
    Downloads metrics objects by calling the appropriate handling function.
    To date onyl from Hugging Face
    """
    # TODO implement other providers
    return get_metrics_to_load_objects_hf(metrics_to_load)


def _get_model(model_full_name: str = None, num_labels: str = None):
    """TODO"""
    # TODO implement other providers
    return get_model_hf(model_full_name, num_labels)


def _set_provider_env(provider: str, provider_param: dict) -> None:
    """Set the environment parameters for the sweep provider"""

    try:
        for k, v in provider_param.items():
            env[k] = v
        env["WANDB_API_KEY"] = get_keyfile_content("wandb")["WANDB_API_KEY"]
        if "APP_DEBUG_IS_ON" in env:
            debug(f"Environment set for {provider=}")
            for s in env:
                if "WANDB_" in s:
                    debug(f"{s}=***") if "API_KEY" in s else debug(f"{s}={env[s]}")
    except Exception as e:
        return e


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

    if "APP_DEBUG_IS_ON" in env:
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
