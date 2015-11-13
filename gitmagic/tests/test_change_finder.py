import unittest
from unittest import mock
import gitmagic

class TestChangeFinder(unittest.TestCase):

    def setUp(self):
        self._repo=mock.Mock()
        self._diff_list = []
        self._repo.head.commit.diff.return_value = self._diff_list

    def test_that_it_returns_the_list_of_changes(self):
        changes = gitmagic.find_changes(self._repo)
        self.assertEquals(list(changes), [])

    def test_that_it_returns_change_objects_for_each_diff(self):
        self._diff_list.append(mock.Mock(a_path="changed_file_name"))
        changes = list(gitmagic.find_changes(self._repo))
        self.assertEquals(len(changes), len(self._diff_list))
        self.assertIsInstance(changes[0], gitmagic.Change)
        self.assertEquals(changes[0].file_name, "changed_file_name")

