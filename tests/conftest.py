#!/usr/bin/env python
"""
A place for pytest fixtures
'Once pytest finds them, it runs those fixtures, captures
what they returned (if anything), and passes those objects
into the test function as arguments.'
Can `return` or `yield` values and have different scopes.
https://docs.pytest.org/en/latest/how-to/fixtures.html
https://docs.pytest.org/en/latest/how-to/writing_plugins.html#conftest-py-plugins
monkeypatch/mock
https://docs.pytest.org/latest/monkeypatch.html
"""

from pytest import fixture
from transformers import BertModel

from app.utils.configure_logging import toggle_global_debug_state

if True:
    toggle_global_debug_state(False)

from app.utils.load_configs import get_defaults, load_defaults_into_load_configs_module


@fixture(scope="function")
def save_dir_fixture() -> str:
    """Returns `save_dir` from the defaults configuration"""

    load_defaults_into_load_configs_module()
    return get_defaults("save_dir")


@fixture(scope="function", params=["accuracy", "recall"])
def metrics_to_test_for(request) -> list[str]:
    """Returns strings of metric names"""
    return request.param


# "distilbert-base-uncased",
# "google/electra-small-discriminator",
# "microsoft/deberta-base",
@fixture(scope="function", params=["bert-base-uncased"])
def model_full_names(request):
    """Returns strings of model names"""
    return request.param


@fixture(scope="function", params=[2])
def num_labels(request):
    """Returns ints of numbers of labels"""
    return request.param


# , DistilBertModel, ElectraModel, DebertaModel
@fixture(scope="function", params=[BertModel])
def subclasses_expected(request):
    """Returns ints of numbers of labels"""
    return request.param
