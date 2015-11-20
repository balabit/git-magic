# Copyright (c) 2015 BalaBit
# All rights reserved.

import gitmagic

class FixupDestinationPicker(object):
    def __init__(self, repo, commit_range):
        self._repo = repo
        self._commit_range = commit_range

    def pick(self, change):
        commits = self._pick_commit_for_change(change)
        for commit in commits:
            if commit not in self._commit_range:
                continue
            return [commit]

        return []

    def _pick_commit_for_change(self, change):
        try:
            return gitmagic.blame(self._repo, change.a_file_name, change.a_hunk)
        except StopIteration:
            return None


def overlaps(start1, end1, start2, end2):
    return start1 >= start2 and start1 <= end2


def blame(repo, filename, hunk):
    commits = []
    (start, end) = hunk
    commit_start = 0
    output = repo.blame(None, filename)
    for commit, lines in output:
        commit_end = commit_start + len( lines )
        if overlaps(start, end, commit_start, commit_end):
            commits.insert(0, commit)
        else:
            commits.append(commit)
        commit_start = commit_end

    return commits

