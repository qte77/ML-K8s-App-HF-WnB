#!/usr/bin/env python
"""
Load components from Hugging Face or local if already present
Hugging Face caches components into '~/.cache/huggingface'
"""
# TODO decorator for get_dataset_hf and get_tokenizer_hf


# from os import walk
# from os.path import join
# from shutil import copyfile
from typing import Any, Union

from datasets import Metric, load_dataset, load_metric
from datasets.dataset_dict import DatasetDict
from transformers import AutoModel, AutoTokenizer

from ..utils.handle_logging import debug_on_global, logging_facility
from ..utils.handle_paths import check_path, create_path, join_path


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
        _log_hf_start_get_dataset(dataset_name, configuration, data_dir_san, dir_exists)

    try:
        dataset = load_dataset(**ds_load_params)
        if not dir_exists:
            if debug_on_global:
                logging_facility("log", f"Saving dataset to {data_dir_san=}")
            dataset.save_to_disk(data_dir_san)
    except Exception as e:
        logging_facility("exception", e)
        return e

    if debug_on_global:
        log_ds_split = "train"
        _log_hf_end_get_dataset(dataset[log_ds_split][:1].items(), log_ds_split)

    return dataset


# FIXME return type `Any`
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
        logging_facility("error", f"{ValueError}. One arg needs to be provided.")
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
        _log_hf_start_get_tokenizer(model_name, save_dir, dir_exists)

    try:
        tokenizer = AutoTokenizer.from_pretrained(**tokenizer_load_params)
        if not dir_exists:
            if debug_on_global:
                logging_facility("log", f"Saving tokenizer to {save_dir=}")
            tokenizer.save_pretrained(save_dir)
    except Exception as e:
        logging_facility("exception", e)
        return e

    if debug_on_global:
        _log_hf_end_get_tokenizer(tokenizer)

    return tokenizer


# FIXME return type `Any`
def get_model_hf(model_full_name: str, num_labels: int, save_dir: str = None) -> Any:
    """
    Downloads the specified model from Hugging Face.

    The models get downloaded to ~/.cache/huggingface first, then saved to {save_dir}
    """

    if not model_full_name and not save_dir:
        logging_facility("error", f"{ValueError}. One arg needs to be provided.")
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
        _log_hf_start_get_model(model_full_name, save_dir, dir_exists)

    try:
        model = AutoModel.from_pretrained(**model_load_params)
        if not dir_exists:
            if debug_on_global:
                logging_facility("log", f"Saving model to {save_dir=}")
            model.save_pretrained(save_dir)
    except Exception as e:
        logging_facility("exception", e)
        return e

    if debug_on_global:
        _log_hf_end_get_model(model.__dict__["config"].architectures)

    return model


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
            logging_facility(
                "log", f"Trying to load HF Metrics Builder Script for {met=}"
            )
        try:
            metric_path_or_name = get_metric_path_or_name_to_load(met, save_dir)
            metric_loaded = load_single_metric(metric_path_or_name)
            metrics_loaded.append(metric_loaded)
        except Exception as e:
            logging_facility("ecxeption", e)
            pass

    return metrics_loaded


def load_single_metric(path: str) -> Union[Metric, Exception]:
    """Loads a single Metric Builder Script from Hugging Face or local path"""

    try:
        return load_metric(path)
    except Exception as e:
        return e


# FIXME more generic save_dir, maybe in  defaults.yml?
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
        logging_facility("error", f"{ValueError}. One arg needs to be provided.")
        return ValueError

    dir = f"{save_dir}/Metrics/{metric_to_load}"

    try:
        return join_path(dir) if check_path(dir) else metric_to_load
    except Exception as e:
        return e


# TODO
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

    return NotImplementedError


# TODO
def load_metric_from_local_path():
    """TODO"""

    # if path_exists:
    #             # FIXME catch empty Metrics folder
    #             path = save_path
    #             # if debug_on_global:
    #             #     logger.debug(f"Loading '{met}' from {save_path=}")

    return NotImplementedError


def _log_hf_start_get_dataset(
    dataset_name: str,
    configuration: str,
    data_dir_san: str,
    dir_exists,
):
    # TODO docstring

    msg_config = f"{configuration=} from " if configuration else ""
    msg_ds_full = f"{msg_config}{dataset_name=}"
    msg_logger = (
        f"Loading local copy of {msg_ds_full} from {data_dir_san=}"
        if dir_exists
        else f"Downloading {msg_ds_full}"
    )
    logging_facility("log", msg_logger)


def _log_hf_end_get_dataset(dict_to_log: dict, log_ds_split: str):
    # TODO docstrings

    logging_facility(
        "log", f"Content of first key of tokenized datasets {log_ds_split} split"
    )
    for _, (k, v) in enumerate(dict_to_log):
        logging_facility("log", f"{k}: {v}".replace('"', '\\"'))


def _log_hf_start_get_tokenizer(model_name: str, save_dir: str, dir_exists: bool):
    # TODO docstrings

    msg_tok = f"tokenizer for {model_name=}"
    msg = (
        f"Loading local copy of {msg_tok} from {save_dir=}"
        if dir_exists
        else f"Downloading {msg_tok}"
    )
    logging_facility("log", msg)


def _log_hf_end_get_tokenizer(tokenizer: Any):
    # TODO docstrings

    tok_msg = "This is a test sentence for the loaded tokenizer."
    tok_res = tokenizer.encode(tok_msg)
    logging_facility("log", f"Tokenizing '{tok_msg}': {tok_res}")


def _log_hf_start_get_model(model_full_name: str, save_dir: str, dir_exists: bool):
    # TODO docstrings

    msg = (
        f"Loading local copy of {model_full_name=} from {save_dir=}"
        if dir_exists
        else f"Downloading {model_full_name=}"
    )
    logging_facility("log", msg)


def _log_hf_end_get_model(model_architectures: list[str]):
    # TODO docstrings

    [logging_facility("log", f"{mod_arch=}") for mod_arch in model_architectures]
