@echo off
rem For Windows to replace Makefile
setlocal enabledelayedexpansion
set LF=^


set "prep=errorcodes!LF!messages!LF!commands"
set options=install update editable wheel test check commit
set options=%options% bump importtime create cleanup

for /f %%p in ("!prep!") do call:%%p
echo %options% | findstr /i "\<%1\>" >nul && goto:run %1

:help
    echo.
    if defined %msg_warning% (
        echo %msg_warning%
        echo.
    )
    echo This file for Windows CMD replaces the Makefile for make
    echo Python needs to be callable and available labels for %%1 are
    echo.
    echo dev %TAB% install %TAB% Installs packages from Pipfile into venv
    echo %TAB% update %TAB% Updates and cleans Pipenv and pre-commit
    echo %TAB% editable %TAB% Installs editable dev [--dev -e .]
    echo %TAB% wheel  %TAB% Builds wheel into ./wheel
	echo %TAB% cleanup %TAB% Deletes the pipenv
    echo qual %TAB% test   %TAB% Runs pytest and coverage report
    echo %TAB% check  %TAB% Runs static tests against codebase
    echo scm %TAB% commit %TAB% %%2 taken as git msg, !!! use with "git msg" !!!
    echo %TAB% bump   %TAB% Bumps the version at "part"
    echo doc %TAB% create %TAB% Creates docu from docstrings
    echo misc %TAB% importtime %TAB% Invokes Python import time and tuna
    echo.
endlocal
exit /b %err_help_called%

:run
    set "label=%1"
    echo starting %label%
    call:%label% %2
    echo done %label%
    endlocal
exit /b %errorlevel%

:install
    pipenv install --dev
	%perun% pre-commit install
	%perun% mypy --install-types --non-interactive
goto:eof

:editable
	echo %msg_not_impl%
    @REM pipenv install --dev -e .
	@REM %perun% pre-commit install
	@REM %perun% mypy --install-types --non-interactive
goto:eof

:wheel
	echo %msg_not_impl%
    @REM %perun% pip wheel . -w wheel
goto:eof

:update
	pipenv lock && pipenv clean && pipenv sync
	%perun% pre-commit autoupdate
goto:eof

:test
	rem https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
    %perun% coverage run -m pytest
    %perun% coverage report
goto:eof

:check:
    echo isort && %perun% isort .
    echo black && %perun% black .
    echo flake8 && %perun% flake8
    echo interrogate && %perun% interrogate
    @REM echo mypy && %perun% mypy .
    setlocal
    set skip=mypy,interrogate
    echo %skip% will be skipped
	echo pre-commit && %perun% pre-commit run --all-files
    endlocal
goto:eof

:commit
	git add .
	@REM %perun% pre-commit run --show-diff-on-failure
    if _%1_ == __ (
        echo %msg_git_no_msg%
        endlocal
        exit /b %err_git_msg_undef%
    ) else (
        setlocal
        set skip=mypy,interrogate
        %perun% git commit -m %1 || echo "%msg_test_fail%"
        endlocal
    )
goto:eof

:bump
    if not _%1_ == __ (
        %perun% bump2version %1
    ) else (
        echo Parameter for 'part' is empty. Exiting.
        exit /b %err_b2v_part_empty%
	)
goto:eof

:importtime
    set "outdir=importtime"
    set "dt=" && set dt=%date:/=-%
    set "tm=" && set tm=%time::=-% && set tm=%tm:~0,8%
    set "ln=%outdir%\%dt%_%tm%_importtime.log"
    if not exist "%outdir%" mkdir "%outdir%"
    %perun% python -X importtime -m app 2>"%ln%"
    %perun% tuna "%ln%"
goto:eof

:create
	echo %msg_not_impl%
    @REM %perun% python -m pandoc write README.md
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
    set err_git_pre_failed=-99
goto:eof

:messages
    set "msg_warning=############ Not Fully Implemented ############"
    set "msg_git_no_msg=No git message provided. Exiting without changes."
    set "msg_not_impl=############ Function Not Implemented ############"
    set "msg_test_fail=Test(s) failed. Nothing commited."
goto:eof

:commands
    set perun=pipenv run
    set "TAB=	"
goto:eof
