#!/usr/bin/env python
"""
Download and save components from providers, e.g. Hugging Face.
Components could be models, datasets, tokenizers, metrics etc.
"""

from dataclasses import dataclass
from os import environ as env
from typing import Final, Union

from datasets.dataset_dict import DatasetDict
from transformers import AutoModelForSequenceClassification, AutoTokenizer

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


# TODO dataclass as code smell ?
# TODO dataclass and FP ?
@dataclass(repr=False, eq=False)
class Paramobj:
    paramobj: dict[str, Union[str, list, dict]]


@dataclass(repr=False, eq=False)  # slots only >=3.10
class Pipeline_Output:
    paramobj: Paramobj
    tokenizer: AutoTokenizer
    dataset_tokenized: DatasetDict
    model: AutoModelForSequenceClassification
    metrics_loaded: list[dict]


def prepare_pipeline(paramobj: Paramobj) -> Pipeline_Output:
    """TODO"""

    provider = paramobj["sweep"]["provider"]
    _set_provider_env(provider, paramobj[provider])

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

    tokenizer = get_tokenizer_hf(
        paramobj["model_full_name"],
        paramobj["save_dir"],
    )

    dataset_tokenized = _get_tokenized_dataset(
        dataset_plain,
        tokenizer,
        paramobj["dataset"]["cols_to_tokenize"],
        paramobj["dataset"]["cols_to_remove"],
    )

    # model = _get_model(paramobj["model_full_name"], paramobj["dataset"]["num_labels"])
    model = ""

    metrics_loaded = _get_metrics_to_load_objects(
        paramobj["metrics"]["metrics_to_load"]
    )

    return Pipeline_Output(
        paramobj, tokenizer, dataset_tokenized, model, metrics_loaded
    )


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
