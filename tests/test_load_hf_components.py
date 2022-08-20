#!/usr/bin/env python
"""Test the load_hf_components"""


# from os import environ as env
from transformers import AutoModel

from app.helper.load_hf_components import get_model_hf

# from pytest import mark


# if "APP_DEBUG_IS_ON" in env:
#     from app.helper.configure_logger import configure_logger, debug_on_global

#     logger = configure_logger()


def test_get_model_hf():
    """TODO"""

    # Arrange
    params = {"model_full_name": "ber_base_uncased", "num_labels": 2}

    # Act
    model = get_model_hf(**params)

    # Assert
    assert type(model) == AutoModel
