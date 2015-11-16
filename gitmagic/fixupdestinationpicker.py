class FixupDestinationPicker(object):
    def __init__(self, repo, commit_range):
        self._repo = repo
        self._commit_range = commit_range

    def pick(self, change):
        commit = self._pick_commit_for_change(change)
        if commit not in self._commit_range:
            return None
        return commit

    def _pick_commit_for_change(self, change):
        try:
            return next(self._repo.iter_commits(paths=change.a_file_name))
        except StopIteration:
            return None

