import unittest
from unittest import mock
from gitmagic import fixup

class TestFixup(unittest.TestCase):
    def setUp(self):
        repomock = mock.Mock()
        repomock.reset.return_value = None
        self.repo = repomock
        fixup(self.repo);

    def test_that_it_resets_the_index(self):
        self.repo.reset.assert_called_with()

