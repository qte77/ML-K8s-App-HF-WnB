#!/usr/bin/env python
# parametrized fixtures with metafunc
# https://medium.com/opsops/deepdive-into-pytest-parametrization-cb21665c05b9
# https://pytest.org/en/7.1.x/example/parametrize.html#deferring-the-setup-of-parametrized-resources
"""Test behavior of load_hf_components"""

from logging import getLogger

from pytest import mark

from app.utils.handle_logging import toggle_global_debug_state

if True:
    toggle_global_debug_state(False)

# delayed loading to set get_and_configure_logger:debug_on_global
from app.pipeline.load_hf_components import get_model_hf

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
