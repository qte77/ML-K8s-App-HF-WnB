@echo off
rem For Windows to replace Makefile
setlocal EnableDelayedExpansion EnableExtensions
set reqs_path=reqs
set LF=^


set "prep=errorcodes!LF!commands!LF!messages"
set options=install update editable wheel reqs cleanup test
set options=%options% check commit push bump log importtime create
set "TAB=	"

set "DEPSMGR_DEFAULT=poetry"
set "DEPSMGR_ALT=pipenv"
echo _%1_ | find /i "_%DEPSMGR_ALT%_" >nul && (
    set DEPSMGR_TOGGLE=%DEPSMGR_ALT%
    set arg_cmd=%2
    set arg_subcmd=%3
) || (
    set DEPSMGR_TOGGLE=%DEPSMGR_DEFAULT%
    set arg_cmd=%1
    set arg_subcmd=%2
)

@REM not defined skips the first command, using echo as first
if not defined %arg_cmd% echo goto:help >nul 2>&1
for /f %%p in ("!prep!") do call:%%p
echo %options% | findstr /i "\<%arg_cmd%\>" >nul && goto:run

:help
    echo.
    if defined !msg_warning! (
        echo %msg_warning%
        echo.
    )
    echo This file for Windows CMD replaces the Makefile for make.
    echo It uses %DEPSMGR_DEFAULT% by default but %DEPSMGR_ALT% is available as toggle.
    echo.
    echo dev %TAB% install %TAB% Installs packages from Pipfile into venv
    echo %TAB% update %TAB% Updates and cleans Pipenv and pre-commit
    echo %TAB% editable %TAB% Installs editable dev
    echo %TAB% wheel  %TAB% Builds wheel into ./wheel
    echo %TAB% %DEPSMGR_ALT% %TAB% Optional as %%1, other args moved right by one
    echo %TAB% cleanup %TAB% Deletes the pipenv
    echo qual %TAB% test   %TAB% Runs pytest and coverage report
    echo %TAB% check  %TAB% Runs static tests against codebase
    echo scm %TAB% commit %TAB% Mandatory %%2=msg, use with "msg" for whitespaces
    echo %TAB% push   %TAB% Adds, commits and pushes if checks and tests passed
    echo %TAB% bump   %TAB% Bumps the version at %%2="part"
    echo %TAB% log    %TAB% Shows one-line git log
    echo docs %TAB% docu   %TAB% Creates docu from /docs
    echo %TAB% docstr %TAB% Creates docu from docstrings
    echo misc %TAB% importtime %TAB% Invokes Python import time and tuna
    echo.
endlocal
exit /b %err_help_called%

:run
    echo %run_start%
    call:%arg_cmd% %arg_subcmd%
    echo %run_end%
    endlocal
exit /b %errorlevel%

:install
    %deps_install%
    call:extras
goto:eof

:editable
	echo %msg_not_impl%
	@REM %deps_editable%
    @REM call:extras
goto:eof

:extras
    %deps_run% pre-commit install
	%deps_run% mypy --install-types --non-interactive
goto:eof

:build
	echo %msg_not_impl%
    @REM pipenv pip wheel . -w wheel
    @REM poetry build
goto:eof

:update
    %deps_update%
	%deps_run% pre-commit autoupdate
goto:eof

:test
	rem https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
    %deps_run% coverage run -m pytest
    %deps_run% coverage report
goto:eof

:check:
    echo hadolint && hadolint docker\Dockerfile
    echo isort && %deps_run% isort .
    echo black && %deps_run% black .
    echo flake8 && %deps_run% flake8
    echo interrogate && %deps_run% interrogate
    echo mypy will be skipped
    @REM echo mypy && %deps_run% mypy .
    setlocal
    set skip=mypy,interrogate
    @REM not defined skips the first command, using echo as first
    if not defined %skip% echo set skip=Nothing >nul 2>&1
    echo pre-commit: %skip% will be skipped
	%deps_run% pre-commit run --all-files
    endlocal
goto:eof

:commit
	git add .
	@REM %deps_run% pre-commit run --show-diff-on-failure
    if _%1_ == __ (
        echo %msg_git_no_msg%
        endlocal
        exit /b %err_git_msg_undef%
    ) else (
        setlocal
        set skip=mypy,interrogate
        call:test
        if ERRORLEVEL 0 (
            %deps_run% git commit -m %1 || echo "%msg_checks_fail%"
        ) else (
            echo Error in pipeline. Nothing commited.
        )
        endlocal
    )
goto:eof

:push
    call:commit %1
    git push && (
        echo Push successful.
    ) || (
        Error occured while pushing. Nothing pushed.
    )
goto:eof

:bump
    if not _%1_ == __ (
        %deps_run% bump2version %1
    ) else (
        echo Parameter for 'part' is empty. Exiting.
        exit /b %err_b2v_part_empty%
	)
goto:eof

:log
    git log --oneline
goto:eof

:importtime
    set "outdir=importtime"
    set "dt=" && set dt=%date:/=-%
    set "tm=" && set tm=%time::=-% && set tm=%tm:~0,8%
    set "ln=%outdir%\%dt%_%tm%_importtime.log"
    if not exist "%outdir%" mkdir "%outdir%"
    %deps_run% python -X importtime -m app 2>"%ln%"
    %deps_run% tuna "%ln%"
goto:eof

:create
	echo %msg_not_impl%
    @REM %deps_run% python -m pandoc write README.md
    @REM docs/header-includes.yaml the_annotated_transformer.md \
    @REM --katex=/usr/local/lib/node_modules/katex/dist/ \
    @REM --output=docs/index.html --to=html5 \
    @REM --css=docs/github.min.css \
    @REM --css=docs/tufte.css \
    @REM --no-highlight --self-contained \
    @REM --metadata pagetitle="The Annotated Transformer" \
    @REM --resource-path=/home/srush/Projects/annotated-transformer/ \
    @REM --indented-code-classes=nohighlight

@REM DEPSMGR_TOGGLE poetry export req
:expreq
    setlocal
    set req=requirements.txt
    set reqdev=requirements-dev.txt
    set req_path=./requirements_other
    set poetryexp=poetry export -f %req% -o
    if not exist "%req_path%" mkdir "%req_path%"
    %poetryexp% "%req_path%/%req%"
    %poetryexp% "%req_path%/%reqdev%" --dev
    endlocal
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
    set err_git_pre_failed=-99
goto:eof

:commands
    if _%DEPSMGR_TOGGLE%_ == _%DEPSMGR_DEFAULT%_ (
        set "depsmgr=%DEPSMGR_DEFAULT%"
        set "deps_install=--no-root"
        set deps_editable=
        set "deps_build=poetry build"
        set "deps_update=poetry update --remove-untracked"
    ) else (
        set "depsmgr=%DEPSMGR_ALT%"
        set "deps_install=-r reqs\Pipfile"
        set deps_editable=--dev -e .
        set "deps_build=pipenv pip wheel . -w wheel"
        set "deps_update=pipenv lock && pipenv clean && pipenv sync"
    )
    set "deps_install=%depsmgr% install %deps_install%"
    set "deps_editable=%depsmgr% install %deps_editable%"
    set "deps_run=%depsmgr% run"
    @REM "set deps_sh=%depsmgr% shell"
goto:eof

:messages
    set "msg_warning=############ Not Fully Implemented ############"
    set "msg_git_no_msg=No git message provided. Exiting without changes."
    set "msg_not_impl=############ Function Not Implemented ############"
    set "msg_checks_fail=Check(s) failed. Nothing commited."
    set "run_start=Starting %arg_cmd%, runtime: %depsmgr%"
    set "run_end=End %arg_cmd%"
goto:eof
