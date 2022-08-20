#!/usr/bin/env python
"""
Load components from Hugging Face or local if already present
Hugging Face caches components into '~/.cache/huggingface'
"""
# TODO decorator for get_dataset_hf and get_tokenizer_hf

from logging import error
from os import environ as env
from typing import Final

from datasets import load_dataset, load_metric
from datasets.dataset_dict import DatasetDict
from transformers import AutoModel, AutoTokenizer

if "APP_DEBUG_IS_ON" in env:
    from logging import debug

    global debug_on_global
    debug_on_global: Final = True

from .check_sanitize_path import check_and_create_path


def get_dataset_hf(
    dataset_name: str, configuration: str = None, save_dir: str = None
) -> DatasetDict:
    """
    Load and save vanilla dataset from Hugging Face

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
            debug(f"Loading local copy of {msg_ds_full} from {save_path=}")
        else:
            debug(f"Downloading {msg_ds_full}")

    try:
        dataset = load_dataset(**ds_load_params)
        if not path_exists:
            if debug_on_global:
                debug(f"Saving dataset to {save_path=}")
            dataset.save_to_disk(save_path)
    except Exception as e:
        error(e)
        return e

    if debug_on_global:
        ds_train_slice = dataset["train"][0]
        debug(f"{ds_train_slice=}")

    return dataset


def get_tokenizer_hf(
    model_name: str = None, save_dir: str = None
) -> AutoTokenizer:  # TODO check return type
    """
    Downloads tokenizer for the specified model.

    A tokenizer converts the input tokens to vocabulary indices and pads the data.
    See [AutoTokenizer Documentation](\
https://huggingface.co/docs/transformers/main/en/\
model_doc/auto#transformers.AutoTokenizer\
).
    """

    save_path, path_exists = check_and_create_path(f"{save_dir}/Tokenizer/{model_name}")
    tokenizer_load_params = {
        "pretrained_model_name_or_path": save_path if path_exists else model_name,
        "truncation": True,
        "padding": True,
    }

    if debug_on_global:
        msg_tok = f"tokenizer for {model_name=}"
        if path_exists:
            debug(f"Loading local copy of {msg_tok} from {save_path=}")
        else:
            debug(f"Downloading {msg_tok}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(**tokenizer_load_params)
        if not path_exists:
            if debug_on_global:
                debug(f"Saving tokenizer to {save_path=}")
            tokenizer.save_pretrained(save_path)
    except Exception as e:
        error(e)
        return e

    if debug_on_global:
        tok_msg = "This is a test sentence for the loaded tokenizer."
        tok_res = tokenizer.encode(tok_msg)
        debug(f"Tokenizing '{tok_msg}': {tok_res}")

    return tokenizer


def get_model_hf(
    model_full_name: str, num_labels: int
) -> AutoModel:  # TODO check return type
    """Downloads specified model"""

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
        debug(f"Downloading {model_full_name=} with {num_labels=}")

    return AutoModel.from_pretrained(model_full_name, num_labels=num_labels)


def get_metrics_to_load_objects_hf(metrics_to_load: list) -> list[dict]:
    """Downloads Hugging Face Metrics Builder Scripts"""

    # TODO metrics save and load locally possible ?
    # TODO error handling, what about empty metrics?

    if debug_on_global:
        debug(f"Loading HF Metrics Builder Scripts for {metrics_to_load!r}")

    metrics_loaded = []

    for met in metrics_to_load:

        if debug_on_global:
            debug(f"Trying to load {met!r}")

        try:
            metrics_loaded.append(load_metric(met))
        except Exception as e:
            # TODO handle error while loading metrics from HF
            error(e)

    return metrics_loaded
