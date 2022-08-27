#!/usr/bin/env python
"""
Download and save components from providers, e.g. Hugging Face.

Components could be models, datasets, tokenizers, metrics etc.
"""

# TODO decorator or facade for handler functions to load provider components,
# e.g. load_hf_components

from dataclasses import dataclass
from logging import getLogger
from os import environ as env
from typing import Union

from datasets import Metric
from datasets.dataset_dict import DatasetDict
from transformers import AutoModel, AutoTokenizer

from .configure_logging import debug_on_global
from .load_configs import get_keyfile_content
from .load_hf_components import (
    get_dataset_hf,
    get_list_of_metrics_to_load,
    get_model_hf,
    get_tokenizer_hf,
)
from .parse_configs_into_paramdict import ParamDict

logger = getLogger(__name__)


@dataclass(repr=False, eq=False)  # slots only >=3.10
class PipelineOutput:
    """
    Holds structured data for the pipeline.

    - `paramdict` as `ParamDict`
    - `tokenizer` as `AutoTokenizer`
    - `dataset_tokenized` as `DatasetDict`
    - `model` as `AutoModel`
    - `metrics_loaded` as `list[dict]`
    """

    paramdict: ParamDict
    tokenizer: AutoTokenizer
    dataset_tokenized: DatasetDict
    model: AutoModel
    metrics_loaded: list[Metric]


def prepare_pipeline(paramdict: ParamDict) -> PipelineOutput:
    """
    Prepares the pipeline by loading Dataset, Tokenizer, Model and Metrics as well
    as setting parameter for the used provider in the system environment.

    Expects a populated `ParamDict` and returns a `PipelineOutput`.
    """

    _set_provider_env(paramdict.sweep["provider"], paramdict.provider_env)
    return _get_large_components(paramdict)


def _get_large_components(paramdict: ParamDict) -> PipelineOutput:
    """Loads components needed for the `PipelineOutput`"""

    dataset_plain = _get_dataset(
        paramdict.dataset["dataset"],
        paramdict.dataset["configuration"],
        paramdict.save_dir,
    )

    tokenizer = _get_tokenizer(
        paramdict.model_full_name,
        paramdict.save_dir,
    )
    # tokenizer = ""

    dataset_tokenized = _get_sanitized_tokenized_dataset(
        dataset_plain,
        tokenizer,
        paramdict.dataset["cols_to_tokenize"],
        paramdict.dataset["cols_to_remove"],
    )
    # dataset_tokenized = ""

    num_labels = len(
        dataset_tokenized["train"].unique(paramdict.dataset["col_to_rename"])
    )
    paramdict.dataset["num_labels"] = num_labels
    if debug_on_global:
        logger.debug(f"The number of unique labels is {num_labels}")

    # paramdict.dataset["num_labels"] = 2

    model = _get_model(paramdict.model_full_name, num_labels, paramdict.save_dir)
    # model = ""

    metrics_loaded = _get_metrics_to_load_objects(
        paramdict.metrics["metrics_to_load"], paramdict.save_dir
    )
    # metrics_loaded = ""

    return PipelineOutput(
        paramdict=paramdict,
        tokenizer=tokenizer,
        dataset_tokenized=dataset_tokenized,
        model=model,
        metrics_loaded=metrics_loaded,
    )


def _get_dataset(
    name: str, configuration: str = None, save_dir: str = None
) -> Union[Exception, DatasetDict]:
    """
    Downloads the dataset by calling the appropriate provider handling function.

    To date only from Hugging Face.
    """
    return get_dataset_hf(name, configuration, save_dir)


def _get_tokenizer(model_full_name: str, save_dir: str = None) -> AutoTokenizer:
    """
    Downloads the tokenizer by calling the appropriate provider handling function.

    To date only from Hugging Face.
    """
    return get_tokenizer_hf(model_full_name, save_dir)


def _get_metrics_to_load_objects(
    metrics_to_load: list, save_dir: str = None
) -> list[Metric]:
    """
    Downloads metrics objects by calling the appropriate provider handling function.

    To date only from Hugging Face.
    """
    return get_list_of_metrics_to_load(metrics_to_load, save_dir)


def _get_model(
    model_full_name: str = None, num_labels: int = None, save_dir: str = None
):
    """
    Downloads the model by calling the appropriate provider handling function.

    To date only from Hugging Face.
    """
    return get_model_hf(model_full_name, num_labels, save_dir)


def _get_sanitized_tokenized_dataset(
    dataset_plain: DatasetDict,
    tokenizer: AutoTokenizer,
    cols_to_tokenize: list[str],
    cols_to_remove: list[str],
) -> DatasetDict:
    """
    Returns the sanitized tokenized dataset stripped of columns not needed.

    TODO save a local copy of the tokenized dataset to avoid overhead
    """

    if debug_on_global:
        logger.debug(
            f"Tokenizing dataset with {len(cols_to_tokenize)} columns to tokenize\
            and \n Removing {cols_to_tokenize=} and {cols_to_remove=} from tokenized\
            dataset"
        )

    try:
        # TODO save local copy of tokenized dataset
        ds_tokenized = (
            _get_raw_tokenized_dataset(dataset_plain, tokenizer, cols_to_tokenize)
            .remove_columns(cols_to_tokenize)
            .remove_columns(cols_to_remove)
        )
        if debug_on_global:
            ds_tokenized_train_slice = ds_tokenized["train"][0]
            logger.debug(f"{ds_tokenized_train_slice=}")
        return ds_tokenized
    except Exception as e:
        logger.error(e)
        return e


def _get_raw_tokenized_dataset(
    dataset_plain: DatasetDict, tokenizer: object, cols_to_tok: list[str]
) -> DatasetDict:
    """Returns the raw tokenized dataset with all columns"""

    def _tokenize(dataset):
        """Tokenizes the columns of `dataset` selected by `cols_to_tok`"""
        cols = [dataset[col] for col in cols_to_tok]
        return tokenizer(*cols, truncation=True)

    return dataset_plain.map(_tokenize, batched=True)


def _set_provider_env(provider: str, provider_env: dict) -> None:
    """Set the environment parameters for the sweep provider including API keys"""

    provider_label = provider.upper()

    try:
        env[f"{provider_label}_API_KEY"] = get_keyfile_content(provider)[
            f"{provider_label}_API_KEY"
        ]
        for k, v in provider_env[provider].items():
            env[k] = v
        if debug_on_global:
            logger.debug(f"Environment set for {provider_label}")
            for s in env:
                if f"{provider_label}_" in s:
                    logger.debug(f"{s}=***") if "API_KEY" in s else logger.debug(
                        f"{s}={env[s]}"
                    )
    except Exception as e:
        logger.error(e)
        return e
