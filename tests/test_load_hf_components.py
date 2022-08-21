#!/usr/bin/env python
"""Test the load_hf_components"""

from pytest import mark
from transformers import BertModel, DistilBertModel, ElectraModel
from transformers.data.datasets.glue import GlueDataset

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
            ],
            [2, 2, 2],
            [BertModel, DistilBertModel, ElectraModel],
        )
    ),
)
def test_get_model_hf(model_full_name, num_labels, type_expected):
    """TODO"""
    # Act
    model = get_model_hf(model_full_name, num_labels)
    logger.debug(f"\n{type(model)=}")
    # Assert
    assert type(model) == type_expected

    GlueDataset.get_labels()
