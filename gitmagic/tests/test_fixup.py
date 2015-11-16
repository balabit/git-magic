import unittest
from unittest import mock
from gitmagic import fixup

class TestFixup(unittest.TestCase):
    def test_that_it_can_be_called(self):
        repo = mock.Mock()
        fixup(repo);

