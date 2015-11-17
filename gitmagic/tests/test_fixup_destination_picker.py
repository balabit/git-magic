import unittest
from unittest import mock
import gitmagic


class TestBlameParser(unittest.TestCase):
    def test_that_it_returns_a_commit_object_from_a_blame_and_a_line_number(self):
        self.commit1 = ['commit1',['line 1', 'line 2', 'line 3']]
        self.commit2 = ['commit2',['line 4', 'line 5', 'line 6']]
        repo = mock.Mock()
        repo.blame.return_value = [self.commit1, self.commit2]
        commit = gitmagic.blame(repo, 'a filename', 2)
        self.assertEquals(commit,self.commit1[0])

class TestFixupDestinationPicker(unittest.TestCase):
    def setUp(self):
        self.changed_file_path = "a_file_path"
        self.matching_commit = self.changed_file_path
        self.repo = mock.Mock()
        self.commit_range = [self.matching_commit, "something else"]
        self.destination_picker = gitmagic.FixupDestinationPicker(self.repo, self.commit_range)

    def test_that_it_picks_a_commit_on_the_changed_file(self):
        self.assertEquals(self._pick_commit_from([self.matching_commit]), [self.matching_commit])

    def test_that_it_picks_a_commit_only_from_the_commit_range(self):
        self.assertEquals(len(self._pick_commit_from(["matching commit not in the range"])), 0)

    def test_that_it_does_not_crash_in_case_of_a_new_file(self):
        self.assertEquals(len(self._pick_commit_from([])), 0)

    def _pick_commit_from(self, commits):
        self.repo.iter_commits.return_value = iter(commits)
        return self.destination_picker.pick(gitmagic.Change(self.changed_file_path, None, None, None, None, None, None))
