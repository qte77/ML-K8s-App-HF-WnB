#!/usr/bin/env python
"""Test the load_hf_components"""

from pytest import mark
from transformers import BertModel, DebertaModel, DistilBertModel, ElectraModel

if True:
    from app.helper.get_and_configure_logger import (
        get_and_configure_logger,
        toggle_global_debug_state,
    )

    toggle_global_debug_state(False)
    logger = get_and_configure_logger()

    # delayed loading to set get_and_configure_logger:debug_on_global
    from app.helper.load_hf_components import get_model_hf


@mark.parametrize(
    "model_full_name, num_labels, type_expected",
    list(
        zip(
            [
                "bert-base-uncased",
                "distilbert-base-uncased",
                "google/electra-small-discriminator",
                "microsoft/deberta-base",
            ],
            [2, 2, 2, 2],
            [BertModel, DistilBertModel, ElectraModel, DebertaModel],
        )
    ),
)
def test_get_model_hf(model_full_name, num_labels, type_expected):
    """TODO"""
    # Act
    model = get_model_hf(model_full_name, num_labels)
    logger.debug("")
    logger.debug(f"{type(model)=}")
    # Assert
    assert type(model) == type_expected
