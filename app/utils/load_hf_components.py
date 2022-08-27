#!/usr/bin/env python
"""
Load components from Hugging Face or local if already present
Hugging Face caches components into '~/.cache/huggingface'
"""
# TODO decorator for get_dataset_hf and get_tokenizer_hf

from logging import getLogger

# from os import walk
# from os.path import join
# from shutil import copyfile
from typing import Any, Union

from datasets import Metric, load_dataset, load_metric
from datasets.dataset_dict import DatasetDict
from transformers import AutoModel, AutoTokenizer

from .configure_logging import debug_on_global
from .handle_paths import check_path, create_path, join_path

logger = getLogger(__name__)


def get_dataset_hf(
    dataset_name: str, configuration: str = None, save_dir: str = None
) -> Union[Exception, DatasetDict]:
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

    dir = f"{save_dir}/Datasets/{dataset_name}/{configuration}"
    dir_exists = check_path(dir)
    data_dir_san = join_path(dir) if dir_exists else ""

    if not dir_exists:
        create_path(dir)

    # TODO load from local dir
    ds_load_params = {
        "path": dataset_name,  # data_dir_san if dir_exists else dataset_name,
        "name": configuration,  # "" if dir_exists else configuration,
        # "data_dir": data_dir_san
    }

    if debug_on_global:
        msg_config = f"{configuration=} from " if configuration else ""
        msg_ds_full = f"{msg_config}{dataset_name=}"
        msg_logger = (
            f"Loading local copy of {msg_ds_full} from {data_dir_san=}"
            if dir_exists
            else f"Downloading {msg_ds_full}"
        )
        logger.debug(f"{ds_load_params=}")
        logger.debug(msg_logger)

    try:
        dataset = load_dataset(**ds_load_params)
        if not dir_exists:
            if debug_on_global:
                logger.debug(f"Saving dataset to {data_dir_san=}")
            dataset.save_to_disk(data_dir_san)
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

    dir = f"{save_dir}/Tokenizer/{model_name}"
    dir_exists = check_path(dir)
    save_dir = join_path(dir) if dir_exists else ""

    if not dir_exists:
        create_path(dir)

    tokenizer_load_params = {
        "pretrained_model_name_or_path": save_dir if dir_exists else model_name,
        "truncation": True,
        "padding": True,
    }

    if debug_on_global:
        msg_tok = f"tokenizer for {model_name=}"
        if dir_exists:
            logger.debug(f"Loading local copy of {msg_tok} from {save_dir=}")
        else:
            logger.debug(f"Downloading {msg_tok}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(**tokenizer_load_params)
        if not dir_exists:
            if debug_on_global:
                logger.debug(f"Saving tokenizer to {save_dir=}")
            tokenizer.save_pretrained(save_dir)
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

    if not model_full_name and not save_dir:
        logger.error(f"{ValueError}. One arg needs to be provided.")
        return ValueError

    dir = f"{save_dir}/Models/{model_full_name}"
    dir_exists = check_path(dir)
    save_dir = join_path(dir) if dir_exists else ""

    if not dir_exists:
        create_path(dir)

    model_load_params = {
        "pretrained_model_name_or_path": save_dir if dir_exists else model_full_name,
        "num_labels": num_labels,
    }

    if debug_on_global:
        msg = (
            f"Loading local copy of {model_full_name=} from {save_dir=}"
            if dir_exists
            else f"Downloading {model_full_name=}"
        )
        logger.debug(msg)

    try:
        model = AutoModel.from_pretrained(**model_load_params)
        if not dir_exists:
            if debug_on_global:
                logger.debug(f"Saving model to {save_dir=}")
            model.save_pretrained(save_dir)
    except Exception as e:
        logger.error(e)
        return e

    return model


# FIXME
def get_list_of_metrics_to_load(
    metrics_to_load: list, save_dir: str = None
) -> list[Metric]:
    """Returns list of Metric-object created by Hugging Face Metrics Builder Scripts"""

    # TODO metrics save and load locally possible ?
    # e.g. datasets.metric.Metric
    # TODO logger.error() handling, what about empty metrics?
    # or met.data_dir

    metrics_loaded = []

    for met in metrics_to_load:
        if debug_on_global:
            logger.debug(f"Trying to load HF Metrics Builder Script for {met=}")
        try:
            metric_path_or_name = get_metric_path_or_name_to_load(met, save_dir)
            metric_loaded = load_single_metric(metric_path_or_name)
            metrics_loaded.append(metric_loaded)
        except Exception as e:
            logger.error(e)
            pass

    return metrics_loaded


def load_single_metric(path: str) -> Union[Metric, Exception]:
    """Loads a single Metric Builder Script from Hugging Face or local path"""

    try:
        return load_metric(path)
    except Exception as e:
        return e


# TODO more generic save_dir, maybe in  defaults.yml?
def get_metric_path_or_name_to_load(
    metric_to_load: str, save_dir: str
) -> Union[str, Exception, ValueError]:
    """
    Checks whether the local metrics folder exists.

    Tests the path f"{save_dir}/Metrics/{metric_to_load}"

    Returns
    - {path} if it exists
    - {metric_to_load}
    """

    if not metric_to_load and not save_dir:
        logger.error(f"{ValueError}. One arg needs to be provided.")
        return ValueError

    dir = f"{save_dir}/Metrics/{metric_to_load}"

    try:
        return join_path(dir) if check_path(dir) else metric_to_load
    except Exception as e:
        return e


def save_metric_to_local_path():
    """TODO"""

    # metrics_cache_dir = "~/.cache/huggingface/modules/datasets_modules/metrics"

    #             dir = sanitize_path(metrics_cache_dir)
    #             for root, _, files in walk(join(dir["dir"], dir["base"])):
    #                 if f"{met}.py" in files:
    #                     # if debug_on_global:
    #                     #     logger.debug(f"Copying '{met}' to {save_path=}")
    #                     for f in files:
    #                         copyfile(join(root, f), join(save_path, f))

    pass


def load_metric_from_local_path():
    """TODO"""

    # if path_exists:
    #             # TODO catch empty Metrics folder
    #             path = save_path
    #             # if debug_on_global:
    #             #     logger.debug(f"Loading '{met}' from {save_path=}")
