import unittest
from unittest import mock
from gitmagic import commit_range

def reverse(lst):
    return list(reversed(lst))

class TestFixup(unittest.TestCase):
    def setUp(self):
        self.left = 'alma'
        self.right = 'right reference'
        self.history = ['initial commit', 'common ancestor', 'commit 1', 'commit 2', self.right]
        self.repo = mock.Mock()
        self.repo.merge_base.return_value = ['common ancestor']
        self.repo.iter_commits.return_value = reverse(self.history)
        self.c_range = commit_range(self.repo, self.left, self.right)

    def test_that_it_returns_only_the_commits_between_the_common_ancestor_and_the_right_reference(self):
        commits_after_common_ancestor = self.history[2:]
        for commit in commits_after_common_ancestor:
            self.assertIn(commit, self.c_range)

        commits_before_common_ancestor = self.history[:2]
        for commit in commits_before_common_ancestor:
            self.assertNotIn(commit, self.c_range)

    def test_that_it_asks_the_merge_base_of_the_left_and_right_reference(self):
        self.repo.merge_base.assert_called_with(self.left, self.right)
