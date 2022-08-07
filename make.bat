@echo off
rem For Windows to replace Makefile
setlocal
set "warning=############ Not Fully Implemented ############"

call:errorcodes
call:messages
call:commands

if _%1_ == _local_install_dev_ goto:run
if _%1_ == _local_update_dev_ goto:run
if _%1_ == _local_test_ goto:run
if _%1_ == _local_static_checks_ goto:run
if _%1_ == _local_commit_ goto:run
if _%1_ == _local_bump_part_ goto:run
if _%1_ == _cleanup_ goto:run

:help
    echo.
    if defined %warning% (
        echo %warning%
        echo.
    )
    echo This file for Windows CMD replaces the Makefile for make
    echo Python needs to be callable and available labels for %%1 are
    echo - local_install_dev -
    echo - local_update_dev -
    echo - local_test -
    echo - local_static_checks -
    echo - local_commit -
    echo - local_bump_part -
	echo - cleanup -
endlocal
exit /b %err_help_called%

:run
    set "label=%1"
    echo starting %label%
    call:%label% %2
    echo done %label%
    endlocal
exit /b

:local_install_dev
    pipenv install --dev
	%perun% pre-commit install
	%perun% mypy --install-types --non-interactive
goto:eof

:local_update_dev
	pipenv update
	%perun% pre-commit autoupdate
goto:eof

:local_test
	echo %msg_not_impl%
	rem https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
goto:eof

:local_static_checks:
    echo isort && %perun% isort .
    echo black && %perun% black .
    echo flake8 && %perun% flake8
    echo mypy && %perun% mypy .
goto:eof

:local_commit
	git add .
	%perun% pre-commit run --show-diff-on-failure
    set git_msg=%1
    set git_msg=%git_msg:"=%
    if defined %git_msg% (
        %perun% git commit -m "%git_msg%"
    ) else (
        echo %msg_git_no_msg%
        endlocal
        exit /b %err_git_msg_undef%
    )
goto:eof

:local_bump_part
	echo %msg_not_impl%
    rem if defined %part% (
    rem    %perun% bump2version %part%
    rem ) else (
    rem    exit /b %err_b2v_part_empty%
	rem )
goto:eof

:cleanup
	echo %msg_not_impl%
    rem rm -rf .pytest_cache .coverage
    rem pipenv --rm
goto:eof

:errorcodes
    set err_help_called=-10
    set err_b2v_part_empty=-20
    set err_git_msg_undef=-30
goto:eof

:messages
    set "msg_git_no_msg=No git message provided. Exiting without changes."
    set "msg_not_impl=############ Function Not Implemented ############"
goto:eof

:commands
    set perun=pipenv run
goto:eof
