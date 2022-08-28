#!/usr/bin/env python
# parametrized fixtures with metafunc
# https://medium.com/opsops/deepdive-into-pytest-parametrization-cb21665c05b9
# https://pytest.org/en/7.1.x/example/parametrize.html#deferring-the-setup-of-parametrized-resources
"""Test load_hf_components"""

from logging import getLogger
from os.path import join, sep

from datasets.metric import Metric
from pytest import mark

from app.utils.handle_logging import toggle_global_debug_state
from app.utils.handle_paths import sanitize_path

if True:
    toggle_global_debug_state(False)

# delayed loading to set get_and_configure_logger:debug_on_global
from app.pipeline.load_hf_components import (
    get_list_of_metrics_to_load,
    get_metric_path_or_name_to_load,
    get_model_hf,
    load_single_metric,
)

logger = getLogger(__name__)


@mark.usefixtures(
    "model_full_names", "num_labels", "subclasses_expected", "save_dir_fixture"
)
def test_get_model_hf(
    model_full_names, num_labels, subclasses_expected, save_dir_fixture
):
    """Expects models of specific subclasses"""

    model = get_model_hf(model_full_names, num_labels, save_dir_fixture)

    assert isinstance(model, subclasses_expected)


# Objectives metrics loading
# 1) load single metric (local or internet) with load_metric(path)
#   if not exists: from internet
# 2) if internet: move metric from local cache to save_dir
# 3) return list[Metric]
@mark.usefixtures("metrics_to_test_for")
def test_load_single_metric(metrics_to_test_for):
    """Expects a single valid Metric-object"""

    metric_loaded = load_single_metric(metrics_to_test_for)

    assert isinstance(metric_loaded, Metric)


@mark.usefixtures("metrics_to_test_for", "save_dir_fixture")
def test_get_metric_path_or_name_to_load(metrics_to_test_for, save_dir_fixture):
    """Expects a valid path to a Metric Builder Script"""

    # TODO test for actual builder script, not only path
    dir = sanitize_path(save_dir_fixture)
    save_dir = join(dir["dir"], dir["base"])
    expected_dir = f"{save_dir}{sep}Metrics{sep}{metrics_to_test_for}"

    returned_dir = get_metric_path_or_name_to_load(
        metrics_to_test_for, save_dir_fixture
    )

    assert returned_dir == expected_dir


@mark.usefixtures("metrics_to_test_for", "save_dir_fixture")
def test_get_list_of_metrics_to_load(metrics_to_test_for, save_dir_fixture):
    """Expects a list of valid Metric-objects"""

    metrics_returned = get_list_of_metrics_to_load(
        [metrics_to_test_for], save_dir_fixture
    )

    # TODO code smell multiple asserts in one test?
    assert isinstance(metrics_returned, list)
    for met in metrics_returned:
        assert isinstance(met, Metric)


# test tokenizer
# from tokenizers import Tokenizer
# assert isinstance(tokenizer._tokenizer, Tokenizer
