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

from app.utils.configure_logging import toggle_global_debug_state

if True:
    toggle_global_debug_state(False)

from app.utils.load_configs import get_defaults, load_defaults_into_load_configs_module


@fixture(scope="function", autouse=True)
def save_dir_fixture() -> str:
    """This is a test fixture with scope 'class' which returns int(1)"""
    load_defaults_into_load_configs_module()
    return get_defaults("save_dir")
