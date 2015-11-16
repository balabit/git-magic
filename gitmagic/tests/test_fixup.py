import unittest
from unittest import mock
from gitmagic import fixup
from gitmagic import find_changes

class TestFixup(unittest.TestCase):

    @mock.patch('gitmagic.find_changes', return_value=iter([]))
    def setUp(self, find_changes_mock):
        repomock = mock.Mock()
        repomock.reset.return_value = None
        self.repo = repomock
        self.find_changes_mock = find_changes_mock
        fixup(self.repo);

    def test_that_it_resets_the_index(self):
        self.repo.reset.assert_called_with()

    def test_that_it_collects_changes(self):
        self.find_changes_mock.assert_called_with(self.repo)

