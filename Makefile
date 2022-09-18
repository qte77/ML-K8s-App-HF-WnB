# https://www.gnu.org/software/make/manual/make.html
# https://www.gnu.org/software/make/manual/html_node/One-Shell.html
# https://makefiletutorial.com/

.PHONY: apply bump check commit full log help commit_msg_check bump_part_check
.DEFAULT_GOAL := help

check_help	= "check\tCheck files and do not apply"
apply_help	= "apply\tCheck files and apply the results"
cmt_usage	= commit msg=\"<message>\"
cmt_error	= "Commit message has to be provided. Usage: $(cmt_usage)"
cmt_help	= "$(cmt_usage)\n\tCheck and commit without staged files"
log_help	= "log\tShow git log oneline"
bump_exp	= major|minor|patch
bump_usage	= bump part=\"<${bump_exp}>\"
bump_error	= "Version part has to be provided. Usage: ${bump_usage}"
bump_help	= "$(bump_usage)\n\tCommit and bump the app version"
git_all_run = $(MAKE) apply && git add . && $(MAKE) bump && git push
git_all_hlp	= "git_all ${cmt_usage} ${bump_usage}\n\tRun \"${git_all_run}\""

apply:
	cirrus run --dirty

bump: bump_part_check commit
	bumpversion "$(firstword $${part})"

check:
	cirrus run

commit: commit_msg_check check
	git commit -m "$(firstword $${msg})"

git_all: commit_msg_check bump_part_check
	@${git_all_run}

log:
	git log --oneline

help:
	@echo -e ${check_help}
	echo -e ${apply_help}
	echo -e ${cmt_help}
	echo -e ${bump_help}
	echo -e ${git_all_hlp}
	echo -e ${log_help}

commit_msg_check:
	@[ "$${msg}" ] || ( echo ${cmt_error}; exit 1 )

.ONESHELL:
bump_part_check:
	@if [ ! $(findstring _${part}_,_$(subst |,_,${bump_exp})_) ]
	then
		echo ${bump_error}
		exit 1
	fi
