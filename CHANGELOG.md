Changelog
===

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Unreleased]
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
