import unittest
from unittest import mock
import gitmagic


class TestBlameParser(unittest.TestCase):
    def setUp(self):
        self.commit1 = ['commit1',['line 1', 'line 2', 'line 3']]
        self.commit2 = ['commit2',['line 4', 'line 5', 'line 6']]
        self.repo = mock.Mock()
        self.repo.blame.return_value = [self.commit1, self.commit2]

    def test_that_it_returns_all_commits_from_the_blame(self):
        commits = self._blame(1, 2)
        self.assertIn(self.commit1[0], commits)
        self.assertIn(self.commit2[0], commits)

    def test_that_it_puts_overlapping_commits_to_the_beginning_of_the_list(self):
        commits = self._blame(4, 4)
        self.assertEquals(self.commit2[0], commits[0])

    def _blame(self, start, end ):
        return gitmagic.blame(self.repo, 'a filename', (start, end))


class TestFixupDestinationPicker(unittest.TestCase):
    def setUp(self):
        self.changed_file_path = "a_file_path"
        self.matching_commit = self.changed_file_path
        self.another_changed_file_path = "another_file_path"
        self.another_matching_commit = self.another_changed_file_path
        self.repo = mock.Mock()
        self.commit_range = [self.matching_commit, self.another_matching_commit]
        self.destination_picker = gitmagic.FixupDestinationPicker(self.repo, self.commit_range)

    def test_that_it_picks_a_commit_on_the_changed_file(self):
        self.assertEquals(self._pick_commit_from([self.matching_commit]), [self.matching_commit])

    def test_that_it_picks_a_commit_only_from_the_commit_range(self):
        self.assertEquals(len(self._pick_commit_from(["matching commit not in the range"])), 0)

    def _pick_commit_from(self, commits):
        with mock.patch('gitmagic.blame') as blame_mock:
            blame_mock.return_value = commits
            return self.destination_picker.pick(
                    gitmagic.Change(
                        self.changed_file_path, "b name",
                        "a content", "b content",
                        (1, 2), (3, 4),
                        "diff"))
