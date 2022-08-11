#!/usr/bin/env python
"""
Load components from Hugging Face or local if already present
"""
# TODO load and save locally, use save path from defaults.yml
from logging import debug, error

from datasets import dataset_dict, load_dataset, load_metric
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def set_debug_state_hf(debug_on: bool = False):
    global debug_on_glob
    debug_on_glob = debug_on


def get_dataset_hf(dataset: str, configuration: str) -> dataset_dict.DatasetDict:
    """TODO"""

    # TODO dataset save and load locally
    # https://huggingface.co/docs/datasets/v1.2.1/loading_datasets.html
    # https://huggingface.co/docs/datasets/loading#local-and-remote-files
    # dataset_dir = f'{save_dir}/Datasets/{dataset}'
    # try:
    #   if not os.path.exists(dataset_dir):
    #     os.makedirs(dataset_dir)
    #     if ds_config == '':
    #       print(orange, f'Downloading and saving dataset "{ds_name}".')
    #       ds = load_dataset(ds_name)
    #     else:
    #       print(orange, f'Downloading and saving dataset \
    #           "{ds_config}" from "{ds_name}".')
    #       ds = load_dataset(ds_name, ds_config)
    #     ds.save_to_disk(dataset_dir)
    #   else:
    #     print(orange, f'Loading dataset from {dataset_dir}')
    #     # if ds_config == '':
    #     data_files = { 'train': 'train' }
    #     ds = load_dataset(path = dataset_dir, data_files = data_files)
    #     # else:
    #     #   ds = load_dataset(path=ds_name, name=ds_config, data_files=dataset_dir)
    # except Exception as e:
    #   print(red, e)

    try:
        if configuration:
            if debug_on_glob:
                debug(f"Downloading {configuration=} from {dataset=}")
            return load_dataset(dataset, configuration)
        else:
            if debug_on_glob:
                debug(f"Downloading dataset {dataset=}")
            return load_dataset(dataset)
    except Exception as e:
        return e


def get_tokenizer_hf(model_full_name: str) -> AutoTokenizer:  # TODO check return type
    """
    Downloads tokenizer for the specified model
    A tokenizer converts the input tokens to vocabulary indices and pads the data
    """

    # TODO tokenizer load and save locally
    # TODO try args max_length=X and fast=False
    # tokenizer_dir = f'{save_dir}/Tokenizer/{modelname}'
    # try:
    #   if not os.path.exists(tokenizer_dir):
    #     print(orange, f'Downloading and saving tokenizer to {tokenizer_dir}')
    #     os.makedirs(tokenizer_dir)
    #     tokenizer = AutoTokenizer.from_pretrained(modelname,
    #       use_fast=True, truncation=True, padding=True)
    #     tokenizer.save_pretrained(tokenizer_dir)
    #   else:
    #     print(orange, f'Loading tokenizer from {tokenizer_dir}')
    #     tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
    # except Exception as e:
    #   print(red, e)

    if debug_on_glob:
        debug(f"Downloading Tokenizer for {model_full_name=}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_full_name, use_fast=True, truncation=True, padding=True
    )

    if debug_on_glob:
        tok_msg = "This is a test sentence."
        tok_res = tokenizer.encode(tok_msg)
        debug(f"Tokenizing '{tok_msg}': {tok_res}")

    return tokenizer


def get_model_hf(
    model_full_name: str, num_labels: int
) -> AutoModelForSequenceClassification:  # TODO check return type
    """Downloads specified model"""

    # ipynb
    # TODO model load and save locally
    # model_dir = f'{save_dir}/Models/{modelname}'
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

    if debug_on_glob:
        debug(f"Downloading {model_full_name=} with {num_labels=}")

    return AutoModelForSequenceClassification.from_pretrained(
        model_full_name, num_labels=num_labels
    )


def get_metrics_to_load_objects_hf(metrics_to_load: list) -> list[dict]:
    """Downloads Hugging Face Metrics Builder Scripts"""

    # TODO metrics save and load locally possible ?

    if debug_on_glob:
        debug(f"Loading HF Metrics Builder Scripts for {metrics_to_load=}")

    metrics_loaded = []

    for met in metrics_to_load:

        if debug_on_glob:
            debug(f"Trying to load {met=}")

        try:
            metrics_loaded.append(load_metric(met))
        except Exception as e:
            error(e)
