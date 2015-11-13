import unittest
from unittest import mock
import gitmagic

class TestChangeFinder(unittest.TestCase):

    def test_that_it_returns_the_list_of_changes(self):
        repo=mock.Mock()
        expected_change_list = []
        repo.head.commit.diff.return_value = expected_change_list
        changes = gitmagic.find_changes(repo)
        self.assertEquals(list(changes), expected_change_list)

