class FixupDestinationPicker(object):
    def __init__(self, repo, commit_range):
        self._repo = repo
        self._commit_range = commit_range

    def pick(self, change):
        commit = self._pick_commit_for_change(change)
        if commit not in self._commit_range:
            return []
        return [commit]

    def _pick_commit_for_change(self, change):
        try:
            return next(self._repo.iter_commits(paths=change.a_file_name))
        except StopIteration:
            return None


def blame(repo, filename, line_number):
    blame_list = _blame_as_list(repo, filename)
    return blame_list[line_number - 1][1]


def _blame_as_list(repo, filename):
    blame_as_list = []
    for commit, lines in repo.blame(None, filename):
        for line in lines:
            blame_as_list.append([line, commit])
    return blame_as_list

