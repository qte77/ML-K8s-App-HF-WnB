@echo off
rem For Windows to replace Makefile
set warning=############ not fully implemented ############

call:errorcodes

if _%1_ == _local_install_dev_ goto:local_install_dev
if _%1_ == _local_update_dev_ goto:local_update_dev
if _%1_ == _local_test_ goto:local_test
if _%1_ == _local_commit_ goto:local_commit
if _%1_ == _cleanup_ goto:cleanup

:help
    echo.
    if defined _%warning%_ (
        echo %warning%
        echo.
    )
    echo This file for Windows CMD replaces the Makefile for make
    echo Python needs to be callable and available labels for %%1 are
    echo - local_install_dev -
    echo - local_update_dev -
    echo - local_test -
    echo - local_commit -
	echo - cleanup -
exit /b %err_help_called%

:setup_local
	echo not implemented
	rem local_install_dev:
	rem pipenv run pre-commit install
	rem pipenv run mypy --install-types --non-interactive
exit /b

:local_update_dev
	echo not implemented
	rem pipenv run pre-commit autoupdate
exit /b

:local_test
	echo not implemented
	rem https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
exit /b

:local_commit:
	echo not implemented
	rem git add .
	rem pipenv run pre-commit run --show-diff-on-failure
	rem git commit -m ""
	rem bump2version %part%
exit /b

:cleanup
    echo cleanup
    rem rm -rf .pytest_cache .coverage
    rem pipenv --rm
exit /b

:errorcodes
    set err_help_called=-1
    set err_b2v_part_empty=-20
goto:eof
