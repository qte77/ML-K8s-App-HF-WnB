@echo off
rem For Windows to replace Makefile
setlocal
set "warning=############ Not Fully Implemented ############"

call:errorcodes
call:messages
call:commands

if _%1_ == _local_install_dev_ goto:run
if _%1_ == _local_update_dev_ goto:run
if _%1_ == _local_install_editable_dev_ goto:run
if _%1_ == _local_wheel_dev_ goto:run
if _%1_ == _local_test_ goto:run
if _%1_ == _local_static_checks_ goto:run
if _%1_ == _local_commit_ goto:run
if _%1_ == _local_bump_part_ goto:run
if _%1_ == _local_import_perf_ goto:run
if _%1_ == _cleanup_ goto:run

:help
    echo.
    if defined %warning% (
        echo %warning%
        echo.
    )
    echo This file for Windows CMD replaces the Makefile for make
    echo Python needs to be callable and available labels for %%1 are
    echo - local_install_dev - Installs packages from Pipfile into venv
    echo - local_update_dev - Updates and cleans Pipenv and pre-commit
    echo - local_install_editable_dev - %msg_not_impl%
    echo - local_wheel_dev - %msg_not_impl%
    echo - local_test - %msg_not_impl%
    echo - local_static_checks - Runs static tests against codebase
    echo - local_commit - %%2 taken as git msg, !!! use with "git msg" !!!
    echo - local_bump_part - Bumps the version at "part"
    echo - local_import_perf - Invokes Python import time and tuna
	echo - cleanup - %msg_not_impl%
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

@REM Installs editable dev [--dev -e .]
@REM :local_build_dev
@REM    pipenv install --dev -e .
@REM 	%perun% pre-commit install
@REM 	%perun% mypy --install-types --non-interactive
@REM goto:eof

@REM Builds wheel into ./wheel
@REM :local_wheel_dev
@REM     %perun% pip wheel . -w wheel
@REM goto:eof

:local_update_dev
	pipenv lock && pipenv clean && pipenv sync
	%perun% pre-commit autoupdate
goto:eof

:local_test
	rem https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
    %perun% python -m pytest
goto:eof

:local_static_checks:
    echo mypy will be skipped
    echo isort && %perun% isort .
    echo black && %perun% black .
    echo flake8 && %perun% flake8
    echo interrogate && %perun% interrogate
    @REM echo mypy && %perun% mypy .
    set skip=mypy
	echo pre-commit && %perun% pre-commit run --all-files
goto:eof

:local_commit
	git add .
	@REM %perun% pre-commit run --show-diff-on-failure
    if _%1_ == __ (
        echo %msg_git_no_msg%
        endlocal
        exit /b %err_git_msg_undef%
    ) else (
        %perun% git commit -m %1 || echo "%msg_test_fail%"
    )
goto:eof

:local_bump_part
    if not _%1_ == __ (
        %perun% bump2version %1
    ) else (
        echo Parameter for 'part' is empty. Exiting.
        exit /b %err_b2v_part_empty%
	)
goto:eof

:local_import_perf
    set "outdir=importtime"
    set "dt=" && set dt=%date:/=-%
    set "tm=" && set tm=%time::=-% && set tm=%tm:~0,8%
    set "ln=%outdir%\%dt%_%tm%_importtime.log"
    if not exist "%outdir%" mkdir "%outdir%"
    %perun% python -X importtime -m app 2>"%ln%"
    %perun% tuna "%ln%"
goto:eof

:local_create_docs
        %perun% python -m pandoc write README.md
        @REM docs/header-includes.yaml the_annotated_transformer.md \
        @REM --katex=/usr/local/lib/node_modules/katex/dist/ \
        @REM --output=docs/index.html --to=html5 \
        @REM --css=docs/github.min.css \
        @REM --css=docs/tufte.css \
        @REM --no-highlight --self-contained \
        @REM --metadata pagetitle="The Annotated Transformer" \
        @REM --resource-path=/home/srush/Projects/annotated-transformer/ \
        @REM --indented-code-classes=nohighlight

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
    set "msg_test_fail=Test(s) failed. Nothing commited."
goto:eof

:commands
    set perun=pipenv run
goto:eof
