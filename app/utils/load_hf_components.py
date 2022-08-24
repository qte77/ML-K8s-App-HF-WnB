#!/usr/bin/env python
"""
Load components from Hugging Face or local if already present
Hugging Face caches components into '~/.cache/huggingface'
"""
# TODO decorator for get_dataset_hf and get_tokenizer_hf

from logging import getLogger
from typing import Any, Union

from datasets import IterableDataset, Metric, load_dataset, load_metric
from datasets.dataset_dict import Dataset, DatasetDict, IterableDatasetDict
from transformers import AutoModel, AutoTokenizer

from .check_and_sanitize_path import check_and_create_path
from .configure_logging import debug_on_global

logger = getLogger(__name__)


def get_dataset_hf(
    dataset_name: str, configuration: str = None, save_dir: str = None
) -> Union[Exception, DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
    """
    Loads a vanilla Hugging Face dataset from a local path if present
    or downloads and saves it to a local path.

    See Hugging Face documentation for\
    [loading datasets](\
https://huggingface.co/docs/datasets/v1.2.1/loading_datasets.html\
)\
    and\
    [local and remote files](\
https://huggingface.co/docs/datasets/loading#local-and-remote-files\
).
    """

    save_path, path_exists = check_and_create_path(
        f"{save_dir}/Datasets/{dataset_name}/{configuration}"
    )
    ds_load_params = {
        "path": dataset_name,
        "name": configuration if configuration else "",
        "data_dir": save_path if path_exists else "",
    }

    if debug_on_global:
        msg_config = f"{configuration=} from " if configuration else ""
        msg_ds_full = f"{msg_config}{dataset_name=}"
        if path_exists:
            logger.debug(f"Loading local copy of {msg_ds_full} from {save_path=}")
        else:
            logger.debug(f"Downloading {msg_ds_full}")

    try:
        dataset = load_dataset(**ds_load_params)
        if not path_exists:
            if debug_on_global:
                logger.debug(f"Saving dataset to {save_path=}")
            dataset.save_to_disk(save_path)
    except Exception as e:
        logger.error(e)
        return e

    if debug_on_global:
        ds_train_slice = dataset["train"][:1]
        logger.debug(f"{ds_train_slice=}")

    return dataset


# TODO check return type
def get_tokenizer_hf(model_name: str = None, save_dir: str = None) -> Any:
    """
    Loads a Hugging Face for the specified model tokenizer from a local path
    if present or downloads and saves it to local path.

    A tokenizer converts the input tokens to vocabulary indices and pads the data.
    See [AutoTokenizer Documentation](\
https://huggingface.co/docs/transformers/main/en/\
model_doc/auto#transformers.AutoTokenizer\
).
    """

    if not model_name and not save_dir:
        logger.error(f"{ValueError}. One arg needs to be provided.")
        return ValueError

    save_path, path_exists = check_and_create_path(f"{save_dir}/Tokenizer/{model_name}")
    tokenizer_load_params = {
        "pretrained_model_name_or_path": save_path if path_exists else model_name,
        "truncation": True,
        "padding": True,
    }

    if debug_on_global:
        msg_tok = f"tokenizer for {model_name=}"
        if path_exists:
            logger.debug(f"Loading local copy of {msg_tok} from {save_path=}")
        else:
            logger.debug(f"Downloading {msg_tok}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(**tokenizer_load_params)
        if not path_exists:
            if debug_on_global:
                logger.debug(f"Saving tokenizer to {save_path=}")
            tokenizer.save_pretrained(save_path)
    except Exception as e:
        logger.error(e)
        return e

    if debug_on_global:
        tok_msg = "This is a test sentence for the loaded tokenizer."
        tok_res = tokenizer.encode(tok_msg)
        logger.debug(f"Tokenizing '{tok_msg}': {tok_res}")

    return tokenizer


# TODO check return type
def get_model_hf(model_full_name: str, num_labels: int, save_dir: str = None) -> Any:
    """
    Downloads the specified model from Hugging Face.

    The models get downloaded to ~/.cache/huggingface first, then saved to {save_dir}
    """

    # check_and_create_path(f"{save_dir}/Models/{modelname}")
    # try:
    # if not os.path.exists(model_dir):
    #     print(green, f'Downloading and saving model to {model_dir}')
    #     os.makedirs(model_dir)
    #     modelobj = AutoModelForSequenceClassification.from_pretrained(
    #       modelname, num_labels=num_labels)
    #     modelobj.save_pretrained(model_dir)
    # else:
    #     print(green, f'Loading model from {model_dir}')
    #     modelobj = AutoModelForSequenceClassification.from_pretrained(model_dir)
    # except Exception as e:
    # print(red, e)

    # model_dir = None; del model_dir

    # colab
    # try:
    #     if not os.path.exists(model_dir):
    #     print(green, f'Downloading and saving model to {model_dir}')
    #     os.makedirs(model_dir)
    #     modelobj = AutoModelForSequenceClassification.from_pretrained(
    #         model_name,
    #         num_labels = num_labels
    #     )
    #     modelobj.save_pretrained(model_dir)
    #     else:
    #     print(green, f'Loading model from {model_dir}')
    #     modelobj = AutoModelForSequenceClassification.from_pretrained(model_dir)
    # except Exception as e:
    #     print(red, e)

    if debug_on_global:
        logger.debug(f"Downloading {model_full_name=} with {num_labels=}")

    return AutoModel.from_pretrained(model_full_name, num_labels=num_labels)


def get_metrics_to_load_objects_hf(metrics_to_load: list) -> list[Metric]:
    """Downloads Hugging Face Metrics Builder Scripts"""

    # TODO metrics save and load locally possible ?
    # TODO logger.error( handling, what about empty metrics?

    if debug_on_global:
        logger.debug(f"Loading HF Metrics Builder Scripts for {metrics_to_load!r}")

    metrics_loaded = []

    for met in metrics_to_load:

        if debug_on_global:
            logger.debug(f"Trying to load {met!r}")

        try:
            metrics_loaded.append(load_metric(met))
        except Exception as e:
            # TODO handle logger.error( while loading metrics from HF
            logger.error(e)

    return metrics_loaded
