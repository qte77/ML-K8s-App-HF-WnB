Changelog
===

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Types of changes:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bugfixes.
- `Security` in case of vulnerabilities.

[Unreleased]
---

### Added

- Hadolint for docker images to pre-commit
  - Commented out because warnings abort pre-commit

### Changed

- Refactored `utils/handle_logging.py` to separate concerns
- Refactored `utils/log_system_info.py`, former name `get_system_info.py`

### Fixed

- Issues with logging multi-line `EOL` and quote-escaping
- Refactored path to `systeminfo.exe` in `utils/get_system_info()`
  - Fixes issue with CodeFactor/Bandit rule `Starting a process with a partial executable path`

[2.7.0] - 2022-08-28
---

### Changed

- Renamed `handle_logging.py`, `app/utils/prepare_pipe_data.py`, `prepare_pipe_params.py`
- Renamed `get_param_dict()` to `get_parameters()`
- Refactored `handle_logging.py`

[2.6.0] - 2022-08-28
---

### Added

- Prepared testing and implementing model training
- Skeleton `utils/build_dir_tree_for_readme.py` for directory tree builder for  app structure inside `README.md`
- CodeFactor badge to `README.md`
- First full TDD functions to get metrics in `load_hf_components`
  - `test_load_single_metric`
  - `test_get_metric_path_to_load`
  - Fixtures with params instead of `@mark.parametrize`
- Domain probing for logging
  - `utils/configure_logging:logging_facility()` as skeleton for domain probing and tested within `app.py`
- [hadolint](https://github.com/hadolint/hadolint#install) to `make.bat:check`

### Changed

- Refactored `__main__.py`
- Refactored `parse_configs_into_paramdict:get_param_dict()`
- Refactored `load_hf_components:get_metrics_to_load_objects_hf()`
- `utils/handle_paths.py`
  - Renamed from `check_and_sanitize_path.py`
  - Separated `check_and_create_path()`
- Refactored `utils/load_hf_components.py`
- Renamed `app/model` to `app/payload`

### Fixed

- Wrong version numbers caused by too many uneccessary bumps
- `Docekrfile` to remidiate CodeFactor.io issues

### Removed

- Mutal exclusive argparse group in `utils/parse_args:parse_args()`

[2.5.0] - 2022-08-26
---

### Added

- `test_load_hf_components:test_get_model_hf()` to assert model type
- `coverage` for reporting of functions covered with `pytest`
- `tests/conftest.py` for pytest fixtures
- `load_hf_components.py`
  - Loading of local models in `get_model_hf()`
  - Local saving and loading of HF Metric Builder Scripts in `get_metrics_to_load_objects_hf()`

### Changed

- Renamed `app/helper`to `app/utils`
- Renamed `utils/configure_logging.py`
- Dataclass `ParamDict` with fields and type annotations
- `README.md`
- `make.bat`

[2.4.0] - 2022-08-21
---

### Added

- `pdoc` for conversion of docstrings to `Pipfile` and `make.bat`
  - Test not successful because of resolving issues
  - E.g. attempted relative import w/o parent package
- Build skeletton
  - Empty `setup.py` to allow for editable build
  - `build-system`, `project` and `setuptools` to `pyproject.toml`
  - Editable installation and build wheel skeleton in `make.bat`

### Changed

- From `pandoc` to `pdoc` because `pandoc` could not be found

[2.3.0] - 2022-08-21
---

### Added

- Tool `interrogate` for coverage of docstrings
  - `pyproject.toml`, `make.bat` and `.pre-commit-config.yaml`
  - Preparation for docgen with `sphinx`
- `tuna` to Pipfile and `make.bat` for visualization of `python -X importtime -m app`

### Changed

- Format of system info output to raw output deliverd by `subprocess:check_output()`
- Moved `toggle_global_sysinfo()` to `get_and_configure_system_info`
- Moved `parse_args()` from `__main__` into `helper/parse_args.py`
- Refactored `__main__`

### Fixed

- Logger instances configured in `logging.conf`in submodules used

[2.2.0] - 2022-08-21
---

### Added

- Local saving and loading of Hugging Face models and Metric Builder Scripts
- Missing docstrings to functions
- `/tests` for prospective TDD with pytest
- `argparse` to `__main__.py`

### Changed

- Moved `check_and_create_path()` to from `load_hf_components` to `check_sanitize_path`
- Refactored `get_dataset_hf` and `get_tokenizer_hf` from `helper/load_hf_components`
- Refactored `prepare_pipeline` from `helper/prepare_ml_input`
- Docstrings aligned according to [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- Setting logger in `main` instead of `app`
- Using logger `simpleExample` from `/helper/configure_logger.py` instead of `root`

[2.1.0] - 2022-08-20
---

### Added

- Decorator for `get_dataset_hf()` and `get_tokenizer_hf()`
- Save and load local models and Metric Builder Scripts
- Dataclass `prepare_ml_input:PipelineOutput` for passing artifacts through pipeline
- Dataclass `prepare_ml_input:ParamDict` for parametrization of the pipeline

### Changed

- Refactored output of `prepare_ml_input:prepare_pipeline()` to dict for `train` and `infer`
- Added parameters to dataclasses in `prepare_ml_input`
- Moved `ParamDict` from `prepare_ml_input` to `parse_configs_into_paramdict`
- Updated TODO in `README.md`

[2.0.0] - 2022-08-15
---

### Added

- Local saving and loading of Hugging Face datasets and tokenizers

### Changed

- Debugging triggered with global final constant inside imports

[1.9.0] - 2022-08-14
---

### Added

- `omegaconf` package to load YAML configuration files
  - Defaults are loaded globally to avoid multiple files operations
  - `OmegaConf.to_object(config)` tor return type `dict`
- System information with `check_output(['systeminfo'])`
- Debug output of environment variables for logging and sweep provider
- `helper/paramobj.dummy.json` added as an example for the data model used by the pipeline
- `.github/` to full app structure in `README.md`
- `helper/sanitize_path.py` for path sanitization
- `APP_SHOW_SYSINFO` to env in `__main__` for debugging

### Changed

- Refactored `main()` in `app.py` for a simpler structure
- Refactored `global debug_on_global` in modules using the `logging` module to `os.environ["APP_DEBUG_IS_ON"]`
  - Also used for conditional import of `logging`
- Keyfile successful loaded with `OmegaConf` inside `helper.load_configs::_load_config()`
- `README.md` for app structure and details

[1.8.0] - 2022-08-10
---

Restructure all functions loading Hugging Face components into own module. Download and optionally save the components for reuse.

### Added

- `load_hf_components.py` containing the functions to load components from Hugging Face
  - HF Metric Builder Scripts not loaded with list comprehension anymore to enable logging
- `load_configs.py:_sanitize_path()` to expand `~` to `$HOME` and return OS-specific paths
- `get_system_info.py` to display information about the system the app is running on

### Changed

- `prepare_ml_input.py` now only calls external functions to load Hugging Face components
- `parse_configs_into_paramdict.py` acts as replacement for `Pipeline`

### Removed

- `Pipeline.py` factored out this object to functional only

[1.7.0] - 2022-08-07
---

### Added

- `dataclasses` to `Pipeline`
  - Exersise stricter type hinting
  - Easier defaulting, comparing and printing of data
  - `fields` possible which are not initialised and represented
  - `order` and sorting of objects possible
  - `frozen`read-only objects possible
  - `__post_init__()` possible
- `@classmethod` to `Pipeline.prepare_ml_input()`

### Changed

- Tokenizer in `prepare_ml_input.py` now with list comprehension inside mapped function
- Global debug state to be set in `__main__.py` or `app.py`

[1.6.0] - 2022-08-07
---

### Added

- `make.bat` as a replacement for `Makefile`

### Changed

- `README` with instructions to install and run

[1.5.0] - 2022-08-07
---

Successful downloads of datasets, models, tokenizer and metrics

### Changed

- Major: `parametrise_pipeline.py`, `prepare_ml_input.py`
- Minor: `app.py`, `Pipeline.py`

[1.4.0] - 2022-08-07
---

First successful creation of config object with loading config files.

[1.3.0] - 2022-08-06
---

Logger added.

### Added

- `config/logging.conf`
- `helper/config_logger.py`

[1.2.0] - 2022-08-06
---

### Changed

- `.bumpversion.cfg` to consider `__version.py` and `_version.py`
- `Pipfile` to include torch==1.11.*, ran pipenv to update `Pipfile.lock`
- `app/app.py` to include first type hinting

[1.1.0] - 2022-08-06
---

### Added

- `app/__main__.py` for later use in package required for tox

### Changed

- `README.md` updated
- `Makefile`, `Pipfile`
- Successful first run of `black`, `flake8`, `mypy`
- Successful first run of `pre-commit` without `flake8`

[1.0.0] - 2022-08-05
---

Major restructuring of the project to align with current qte77's SOTA project structure.

### Added

- Project: `pyproject.toml`
- App: `__version__.py`, `py.typed`
- Tools config: `.bumpversion`, `flake8`, `.markdownlint.yml`, `.pre-commit-config.yaml`
- gh-actions: `dependabot.yml`

### Changed

- Project: `Pipfile`, `Pipfile.lock`
- App: `_version.py`
- git: `.gitignore`, `.gitmessage`
- MDs to adopt markdownlint.yml

### Removed

- git: `ISSUE_TEMPLATE.md`

[0.3.0] - 2022-07-23
---

### Added

- Pipfile and Pifile.lock
- ISSUE_TEMPLATE.md

### Changed

- App structure
- .gitignore and .gitmessage

### Removed

- .python-version because Pipfile tracks Python version

[0.2.0] - 2022-07-20
---

### Added

- ./app/_version.py to track app version

### Changed

- CHANGELOG.md
- ./kubernetes/overlay renamed to ./kubernetes/overlays

[0.1.0] - 2022-07-20
---

### Added

- CHANGELOG.md to keep curated, annotated and chronologic list of changes

### Changed

- .gitignore for vscode
- README.md
- /app/Pipfile instead of requirements.txt

### Removed

- /app/requirements.txt as obsolete
- /app/requirements-dev.txt as obsolete
