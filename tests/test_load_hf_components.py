#!/usr/bin/env python
"""Test the load_hf_components"""

from logging import getLogger
from os.path import join, sep

from datasets.metric import Metric
from pytest import mark
from transformers import BertModel  # , DebertaModel, DistilBertModel, ElectraModel

from app.utils.configure_logging import toggle_global_debug_state
from app.utils.handle_paths import sanitize_path

if True:
    toggle_global_debug_state(False)

# delayed loading to set get_and_configure_logger:debug_on_global
from app.utils.load_hf_components import (
    get_metric_path_to_load,
    get_model_hf,
    load_single_metric,
)

logger = getLogger(__name__)


@mark.usefixtures("save_dir_fixture")
@mark.parametrize(
    ["model_full_name", "num_labels", "subclass_expected"],
    list(
        zip(
            [
                "bert-base-uncased",
                # "distilbert-base-uncased",
                # "google/electra-small-discriminator",
                # "microsoft/deberta-base",
            ],
            [2],  # , 2, 2, 2],
            [BertModel],  # , DistilBertModel, ElectraModel, DebertaModel],
        )
    ),
)
def test_get_model_hf(model_full_name, num_labels, subclass_expected, save_dir_fixture):
    """TODO"""
    model = get_model_hf(model_full_name, num_labels, save_dir_fixture)
    assert isinstance(model, subclass_expected)


# Objectives metrics loading
# 1) load single metric (local or internet) with load_metric(path)
#   if not exists: from internet
# 2) if internet: move metric from local cache to save_dir
# 3) return list[Metric]
@mark.parametrize(
    "metric_name", ["accuracy"]  # , "precision", "recall", "f1", "mse", "mae"]
)
def test_load_single_metric(metric_name):
    """TODO"""
    metric_loaded = load_single_metric(metric_name)
    assert isinstance(metric_loaded, Metric)


@mark.usefixtures("save_dir_fixture")
@mark.parametrize("metric_name", ["accuracy"])
def test_get_metric_path_to_load(metric_name, save_dir_fixture):
    """TODO"""

    dir = sanitize_path(save_dir_fixture)
    save_dir = join(dir["dir"], dir["base"])
    expected_dir = f"{save_dir}{sep}Metrics{sep}{metric_name}"

    returned_dir = get_metric_path_to_load(metric_name, save_dir_fixture)

    assert returned_dir == expected_dir


# def test_get_metrics_to_load_objects_hf(metrics_to_load, save_dir):
#     """TODO"""
#     # Act
#     model = get_metrics_to_load_objects_hf(metrics_to_load, save_dir)
#     logger.debug("")
#     logger.debug(f"{type(model)=}")
#     # Assert
#     assert type(model) == Metric

# TODO parametrized fixtures
# class TimeLine:
#     def __init__(self, instances=[0, 0, 0]):
#         self.instances = instances


# @fixture(params=[[-2, 2, 30], [2, 4, 0], [6, 8, 10]])
# def timeline(request):
#     return TimeLine(request.param)


# def test_timeline(timeline):
#     for instance in timeline.instances:
#         assert instance % 2 == 0
