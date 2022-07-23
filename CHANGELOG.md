# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2022-07-23

### Added

- Pipfile and Pifile.lock
- ISSUE_TEMPLATE.md

### Changed

- App structure
- .gitignore and .gitmessage

### Removed

- .python-version because Pipfile tracks Python version

## [0.2.0] - 2022-07-20

### Added

- ./app/_version.py to track app version

### Changed

- CHANGELOG.md
- ./kubernetes/overlay renamed to ./kubernetes/overlays

## [0.1.0] - 2022-07-20

### Added

- CHANGELOG.md to keep curated, annotated and chronologic list of changes

### Changed

- .gitignore for vscode
- README.md
- /app/Pipfile instead of requirements.txt

### Removed

- /app/requirements.txt as obsolete
- /app/requirements-dev.txt as obsolete