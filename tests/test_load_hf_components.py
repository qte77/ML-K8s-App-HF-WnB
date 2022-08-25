#!/usr/bin/env python
"""Test the load_hf_components"""

from logging import getLogger

from pytest import fixture, mark
from transformers import BertModel, DebertaModel, DistilBertModel, ElectraModel

from app.utils.configure_logging import toggle_global_debug_state

if True:
    toggle_global_debug_state(False)

# delayed loading to set get_and_configure_logger:debug_on_global
from app.utils.load_hf_components import get_metrics_to_load_objects_hf, get_model_hf

logger = getLogger(__name__)


# @mark.usefixtures("save_dir_fixture")
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
def test_get_model_hf(model_full_name, num_labels, save_dir_fixture, type_expected):
    """TODO"""
    # Act
    model = get_model_hf(model_full_name, num_labels, save_dir_fixture)
    # logger.debug("")
    # logger.debug(f"{type(model)=}")
    # Assert
    assert type(model) == type_expected


def test_get_metrics_to_load_objects_hf(
    model_full_name, num_labels, save_dir_fixture, type_expected
):
    """TODO"""
    # Act
    model = get_metrics_to_load_objects_hf(
        model_full_name, num_labels, save_dir_fixture
    )
    # logger.debug("")
    # logger.debug(f"{type(model)=}")
    # Assert
    assert type(model) == type_expected


class TimeLine:
    def __init__(self, instances=[0, 0, 0]):
        self.instances = instances


@fixture(params=[[-2, 2, 30], [2, 4, 0], [6, 8, 10]])
def timeline(request):
    return TimeLine(request.param)


def test_timeline(timeline):
    for instance in timeline.instances:
        assert instance % 2 == 0
