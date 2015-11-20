# Copyright (c) 2015 BalaBit
# All rights reserved.

def commit_range(repo, left='master', right='HEAD'):
    range = []
    common_ancestor = repo.merge_base(left, right)[0]

    for commit in repo.iter_commits(None):
        if commit == common_ancestor:
            break
        range.append(commit)

    return range
