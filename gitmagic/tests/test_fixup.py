import unittest
from unittest import mock
from gitmagic import fixup
from gitmagic import find_changes
from gitmagic import Change

class TestFixup(unittest.TestCase):

    @mock.patch('gitmagic.find_changes')
    def setUp(self, find_changes ):

        self.first_change = mock.Mock()
        find_changes.return_value = iter([self.first_change])
        self.find_changes = find_changes

        repo = mock.Mock()
        self.repo = repo

        self.destination_commit = mock.Mock()
        self.destination_commit.message.return_value = "a commit message"
        destination_picker = mock.Mock()
        destination_picker.pick.return_value = self.destination_commit
        self.destination_picker = destination_picker

        self.destination_picker = destination_picker
        fixup(self.repo, self.destination_picker);

    def test_that_it_resets_the_index(self):
        self.repo.reset.assert_called_with()

    def test_that_it_collects_changes(self):
        self.find_changes.assert_called_with(self.repo)

    def test_that_it_picks_destination_commit_for_each_change_object(self):
        self.destination_picker.pick.assert_called_with(self.first_change)

    def test_that_it_commits_the_change_with_the_proper_fixup_message(self):
        self.destination_commit.message.assert_called_with()
        self.repo.index.commit.assert_called_with(message = "fixup! {}".format(self.destination_commit.message.return_value))

