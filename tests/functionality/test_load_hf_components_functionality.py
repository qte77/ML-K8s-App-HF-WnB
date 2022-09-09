#!/usr/bin/env python
""""Test functionality of load_hf_components"""

from logging import getLogger
from os.path import join

from datasets.metric import Metric
from pytest import mark

from app.utils.handle_logging import toggle_global_debug_state
from app.utils.handle_paths import sanitize_path

if True:
    toggle_global_debug_state(False)

# delayed loading to set get_and_configure_logger:debug_on_global
from app.pipeline.load_hf_components import (  # _load_single_metric,
    _get_metric_path_or_name_to_load,
    get_list_of_metrics_to_load,
)

logger = getLogger(__name__)


@mark.usefixtures("metrics_to_test_for", "save_dir_fixture")
def test__get_metric_path_or_name_to_load(metrics_to_test_for, save_dir_fixture):
    """Expects a valid path to a Metric Builder Script"""

    # TODO test for actual builder script, not only path
    dir = sanitize_path(save_dir_fixture)
    save_dir = join(dir["dir"], dir["base"])
    expected_dir = join(save_dir, "Metrics", metrics_to_test_for)
    returned_dir = _get_metric_path_or_name_to_load(
        metrics_to_test_for, save_dir_fixture
    )

    print("")
    print(expected_dir)
    print(returned_dir)

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
