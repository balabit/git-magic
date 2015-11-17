def commit_range(repo, left='master', right='HEAD'):
    range = []
    common_ancestor = repo.merge_base(left, right)

    for commit in repo.iter_commits(None):
        if commit == common_ancestor:
            break
        range.append(commit)

    return range
