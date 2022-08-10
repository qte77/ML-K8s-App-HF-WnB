#!/usr/bin/env python
"""
Load components from Hugging Face or local if already present
"""
from logging import debug

from datasets import dataset_dict, load_dataset, load_metric
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def set_debug_state_hf(debug_on: bool = False):
    global debug_state
    debug_state = debug_on


def get_dataset(dataset: str, configuration: str) -> dataset_dict.DatasetDict:
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


def get_tokenizer(model_full_name: str) -> AutoTokenizer:  # TODO check return type
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


def get_model(
    model_full_name: str, num_labels: int
) -> AutoModelForSequenceClassification:  # TODO check return type
    """Downloads specified model"""

    if debug_state:
        debug(f"Downloading {model_full_name=} with {num_labels=}")

    return AutoModelForSequenceClassification.from_pretrained(
        model_full_name, num_labels=num_labels
    )


def get_metrics_to_load_objects_hf(metrics_to_load: list) -> list[dict]:
    """Downloads Hugging Face Metrics Builder Scripts"""

    if debug_state:
        debug(f"Loading HF Metrics Builder Scripts for {metrics_to_load}")

    try:
        return [load_metric(met) for met in metrics_to_load]
    except Exception as e:
        return e
