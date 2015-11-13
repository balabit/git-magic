class FixupDestinationPicker(object):
    def __init__(self, repo, commit_range):
        self._repo = repo
        self._commit_range = commit_range

    def pick(self, change):
        return self._pick_commit_for_change(change)


    def _pick_commit_for_change(self, change):
        gen = self._repo.commit.iter_items(self._repo, self._repo.head, paths=change.file_name)
        return next(gen)

