#!/bin/bash
trap "rm -f /tmp/$$.*" EXIT

function transplant() # <from> <to> <branch>
{
    OLD_TRUNK=$1
    NEW_TRUNK=$2
    BRANCH=$3

    # 1. get branch revisions
    REV_FILE="/tmp/$$.rev-list.$BRANCH"
    git rev-list $BRANCH ^$OLD_TRUNK > "$REV_FILE" || exit $?
    OLD_BRANCH_FORK=$(tail -1 "$REV_FILE")
    OLD_BRANCH_HEAD=$(head -1 "$REV_FILE")
    COMMON_ANCESTOR="${OLD_BRANCH_FORK}^"

    # 2. transplant this branch
    git rebase --onto $NEW_TRUNK $COMMON_ANCESTOR $BRANCH

    # 3. find other sub-branches:
    git branch --contains $OLD_BRANCH_FORK | while read sub;
    do
        # 4. figure out where the sub-branch diverges,
        # relative to the (old) branch head
        DISTANCE=$(git rev-list $OLD_BRANCH_HEAD ^$sub | wc -l)

        # 5. transplant sub-branch from old branch to new branch, attaching at
        # same number of commits before new HEAD
        transplant $OLD_BRANCH_HEAD ${BRANCH}~$DISTANCE  $sub
    done
}

transplant $1 $2 $3
