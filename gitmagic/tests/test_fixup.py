import unittest
from unittest import mock
from gitmagic import fixup
from gitmagic import find_changes
from gitmagic import Change

class TestFixup(unittest.TestCase):

    def setUp(self):
        self.repo = mock.Mock()
        self.destination_commit = mock.Mock()
        self.destination_commit.message = "a commit message"
        self.destination_picker = mock.Mock()
        self.destination_picker.pick.return_value = self.destination_commit

        self.first_change = mock.Mock()
        self.find_changes = mock.Mock()
        self.find_changes.return_value = iter([self.first_change])
        fixup(self.repo, self.destination_picker, self.find_changes);

    def test_that_it_resets_the_index(self):
        self.repo.index.reset.assert_called_with()

    def test_that_it_collects_changes(self):
        self.find_changes.assert_called_with(self.repo)

    def test_that_it_picks_destination_commit_for_each_change_object(self):
        self.destination_picker.pick.assert_called_with(self.first_change)

    def test_that_it_commits_the_change_with_the_proper_fixup_message(self):
        self.repo.index.commit.assert_called_with(message = "fixup! {}".format(self.destination_commit.message))

