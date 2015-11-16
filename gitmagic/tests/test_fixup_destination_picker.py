import unittest
from unittest import mock
import gitmagic

class TestFixupDestinationPicker(unittest.TestCase):
    def setUp(self):
        self.changed_file_path = "a_file_path"
        self.matching_commit = self.changed_file_path
        self.repo = mock.Mock()
        self.commit_range = [self.matching_commit, "something else"]
        self.destination_picker = gitmagic.FixupDestinationPicker(self.repo, self.commit_range)

    def test_that_it_picks_a_commit_on_the_changed_file(self):
        self.assertEquals(self._pick_commit_from([self.matching_commit]), self.matching_commit)

    def test_that_it_picks_a_commit_only_from_the_commit_range(self):
        self.assertIsNone(self._pick_commit_from(["matching commit not in the range"]))

    def test_that_it_does_not_crash_in_case_of_a_new_file(self):
        self.assertIsNone(self._pick_commit_from([]))

    def _pick_commit_from(self, commits):
        self.repo.iter_commits.return_value = iter(commits)
        return self.destination_picker.pick(gitmagic.Change(self.changed_file_path))

