# https://www.gnu.org/software/make/manual/make.html
# https://www.gnu.org/software/make/manual/html_node/One-Shell.html
# https://makefiletutorial.com/

.PHONY: apply bump check commit full log help commit_msg_check bump_part_check
.DEFAULT_GOAL := help

full_help	= full: Run apply, git add, bump and push
check_help	= check: Check files and do not apply
apply_help	= apply: Check files and apply the results
cmt_usage	= 'commit msg="<message>"'
cmt_empty	= Commit message has to be provided. Usage: $(cmt_usage)
cmt_help	= $(cmt_usage): Check and commit without staged files
bump_exp	= major|minor|patch
bump_usage	= bump part=<${bump_exp}>
bump_empty	= Version part has to be provided. Usage: ${bump_usage}
bump_help	= $(bump_usage): Bump the app version
log_help	= log: Show git log oneline

apply:
	cirrus run --dirty

bump: bump_part_check commit
	bumpversion ${part}

check:
	cirrus run

commit: commit_msg_check check
	git commit -m "$(firstword $${msg})"

full: commit_msg_check
	apply
	git add .
	bump
	git push

log:
	git log --oneline

help:
	@echo ${full_help}
	echo ${check_help}
	echo ${apply_help}
	echo ${cmt_help}
	echo ${bump_help}

commit_msg_check:
	@[ "$${msg}" ] || ( echo ${cmt_empty}; exit 1 )

.ONESHELL:
bump_part_check:
	@if [ ! $(findstring _${part}_,_$(subst |,_,${bump_exp})_) ]
	then
		echo ${bump_empty}
		exit 1
	fi
