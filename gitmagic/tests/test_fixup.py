import unittest
from unittest import mock
from gitmagic import fixup
from gitmagic import find_changes
from gitmagic import Change
from io import StringIO

class CommonFixupTest(unittest.TestCase):
    def setUp(self):
        self.repo = mock.Mock()
        self.destination_commit = mock.Mock()
        self.destination_commit.message = "a commit message"
        self.destination_commit.hexsha = "commit sha"
        self.destination_commit.summary = "commit sum"
        self.first_change = mock.Mock()
        self.first_change.diff = "the diff"
        self.find_changes = mock.Mock()
        self.find_changes.return_value = iter([self.first_change])
        self.destination_picker = mock.Mock()
        self.do_set_up()
        with mock.patch( "git.cmd.Git" ) as GitMock:
            instance_mock = mock.Mock()
            instance_mock.execute.return_value = None
            GitMock.return_value = instance_mock
            fixup(self.repo, self.destination_picker, self.find_changes)
            GitMock.assert_called_with(self.repo.working_dir)

class TestFixupWithoutDestinationCommit(CommonFixupTest):
    def do_set_up(self):
        self.destination_picker.pick.return_value = []

    def test_that_it_creates_a_new_commit_for_changes_without_a_destination(self):
        self.repo.index.commit.assert_called_with( message="WARNING: no destination commit" )


class TestFixup(CommonFixupTest):

    def do_set_up(self):
        self.destination_picker.pick.return_value = [self.destination_commit]

    def test_that_it_resets_the_index(self):
        self.repo.index.reset.assert_called_with()

    def test_that_it_collects_changes(self):
        self.find_changes.assert_called_with(self.repo)

    def test_that_it_picks_destination_commit_for_each_change_object(self):
        self.destination_picker.pick.assert_called_with(self.first_change)

    def test_that_it_commits_the_change_with_the_proper_fixup_message(self):
        self.repo.index.commit.assert_called_with(message = "fixup! {}".format(self.destination_commit.message))

