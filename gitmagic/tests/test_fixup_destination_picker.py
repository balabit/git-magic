import unittest
from unittest import mock
import gitmagic

class TestFixupDestinationPicker(unittest.TestCase):
    def setUp(self):
        self.changed_file_path = "a_file_path"
        self.commit_object = self.changed_file_path
        self.repo = mock.Mock()
        self.repo.commit.iter_items.return_value = iter( [ self.commit_object ] )
        self.commit_range = [self.commit_object, "something else"]
        self.destination_picker = gitmagic.FixupDestinationPicker(self.repo, self.commit_range)

    def test_that_it_picks_a_commit_on_the_changed_file(self):
        commit = self.destination_picker.pick(gitmagic.Change(self.changed_file_path))
        self.assertEquals(commit, self.commit_object)

