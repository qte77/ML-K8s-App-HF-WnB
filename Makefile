# https://www.gnu.org/software/make/manual/make.html
# https://www.gnu.org/software/make/manual/html_node/One-Shell.html
# https://makefiletutorial.com/

.PHONY: all apply check commit check_message push log bump help
.DEFAULT_GOAL := help

all_run		= apply commit bump push
all_help	= "Run '${all_run}': make all"
check_help	= Check files: make check
apply_help	= Apply checks to files: make apply
cmt_usage	= 'make commit msg="<message>"'
cmt_empty	= Commit message has to be provided. Usage: $(cmt_usage)
cmt_help	= Check and commit without staged files: $(cmt_usage)
part_exp	= major|minor|patch
part_usage	= 'make bump part=<${part_exp}>'
part_empty	= Version part has to be provied. Usage: ${part_usage}
part_help	= Bump the app version: $(part_usage)
push_help	= Check and push without commit: make push

all: commit_msg_check ${all_run}

apply:
	cirrus run --dirty

bump: bump_part_check commit
	bumpversion ${part}

check:
	cirrus run

commit: commit_msg_check check
	git commit -m "$(firstword $${msg})"

log:
	git log --oneline

push: check
	git push

help:
	@echo ${all_help}
	echo ${check_help}
	echo ${apply_help}
	echo ${cmt_help}
	echo ${push_help}
	echo ${part_help}

commit_msg_check:
	@[ "$${msg}" ] || ( echo ${cmt_empty}; exit 1 )

.ONESHELL:
bump_part_check:
	@if [ ! $(findstring _${part}_,_$(subst |,_,${part_exp})_) ]
	then
		echo ${part_empty}
		exit 1
	fi
