#!/usr/bin/env python
"""
Download and save components from providers, e.g. Hugging Face.
Components could be models, datasets, tokenizers, metrics etc.
"""

# TODO return None or Exception ?
# TODO load local versions of models, datasets, metrics and tokenizer if not cached
# TODO function def with actual objects, not placeholder 'object'
from os import environ as env
from typing import Final, Union

from datasets.dataset_dict import DatasetDict
from transformers import AutoTokenizer

if "APP_DEBUG_IS_ON" in env:
    from logging import debug

    global debug_on_global
    debug_on_global: Final = True

from .load_configs import get_keyfile_content
from .load_hf_components import (
    get_dataset_hf,
    get_metrics_to_load_objects_hf,
    get_model_hf,
    get_tokenizer_hf,
)


def prepare_pipeline(paramobj: dict) -> Union[dict, DatasetDict]:
    """TODO"""

    dataset_plain = get_dataset_hf(
        paramobj["dataset"]["dataset"],
        paramobj["dataset"]["configuration"],
        paramobj["save_dir"],
    )
    num_labels = len(
        dataset_plain["train"].unique(paramobj["dataset"]["col_to_rename"])
    )
    paramobj["dataset"]["num_labels"] = num_labels
    if debug_on_global:
        debug(f"The number of unique labels is {num_labels}")

    _ = _get_tokenized_dataset(
        dataset_plain,
        get_tokenizer_hf(
            paramobj["model_full_name"],
            paramobj["save_dir"],
        ),
        paramobj["dataset"]["cols_to_tokenize"],
        paramobj["dataset"]["cols_to_remove"],
    )

    # paramobj["metrics"]["metrics_loaded"] = _get_metrics_to_load_objects(
    #     paramobj["metrics"]["metrics_to_load"]
    # )
    # _get_model(paramobj["model_full_name"], paramobj["dataset"]["num_labels"])
    # provider = paramobj["sweep"]["provider"]
    # _set_provider_env(provider, paramobj[provider])

    return paramobj


def _get_tokenized_dataset(
    dataset_plain: DatasetDict,
    tokenizer: AutoTokenizer,
    cols_to_tokenize: list[str],
    cols_to_remove: list[str],
) -> DatasetDict:
    """TODO"""

    if debug_on_global:
        debug(
            f"Tokenizing dataset with {len(cols_to_tokenize)} columns to tokenize\
            and \n Removing {cols_to_tokenize=} and {cols_to_remove=} from tokenized\
            dataset"
        )

    try:
        ds_tokenized = (
            _get_raw_tokenized_dataset(dataset_plain, tokenizer, cols_to_tokenize)
            .remove_columns(cols_to_tokenize)
            .remove_columns(cols_to_remove)
        )
        if debug_on_global:
            ds_tokenized_train_slice = ds_tokenized["train"][0]
            print(f"{ds_tokenized_train_slice=}")
        return ds_tokenized
    except Exception as e:
        return e


def _get_raw_tokenized_dataset(
    dataset_plain: DatasetDict, tokenizer: object, cols_to_tok: list[str]
) -> DatasetDict:
    """Returns tokenized dataset"""

    def _tokenize(ds):
        cols = [ds[col] for col in cols_to_tok]
        return tokenizer(*cols, truncation=True)

    return dataset_plain.map(_tokenize, batched=True)


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
        if debug_on_global:
            debug(f"Environment set for {provider=}")
            for s in env:
                if "WANDB_" in s:
                    debug(f"{s}=***") if "API_KEY" in s else debug(f"{s}={env[s]}")
    except Exception as e:
        return e
