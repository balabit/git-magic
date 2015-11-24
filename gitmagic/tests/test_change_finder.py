import unittest
from unittest import mock

import git
import gitmagic


class TestChangeFinder(unittest.TestCase):
    B_FILE_CONTENT = mock.Mock(
        read=mock.Mock(return_value='line1\nlineb\nline3')
    )

    def setUp(self):
        self._repo = mock.Mock(spec=git.repo.Repo)
        self._diff_list = []
        self._diff_list_on_second_call = []
        self._repo.head.commit.diff.side_effect = [self._diff_list, self._diff_list_on_second_call, []]
        self._diff_mock = mock.Mock(
            a_path="changed_file_name",
            b_path="changed_file_name",
            a_blob=mock.Mock(
                data_stream=mock.Mock(
                    read=mock.Mock(return_value=b'line1\nlinea\nline3'))),
        )

    @mock.patch('builtins.open', mock.Mock(return_value=B_FILE_CONTENT))
    def test_that_it_returns_empty_list_if_there_are_no_changes(self):
        changes = gitmagic.find_changes(self._repo)
        self.assertEquals(list(changes), [])

    @mock.patch('builtins.open', mock.Mock(return_value=B_FILE_CONTENT))
    def test_that_it_returns_change_objects_for_each_diff(self):
        self._diff_list.append(self._diff_mock)
        changes = list(gitmagic.find_changes(self._repo))
        self.assertEquals(len(changes), len(self._diff_list))
        self.assertIsInstance(changes[0], gitmagic.Change)
        self.assertEquals(changes[0].a_file_name, "changed_file_name")
        self.assertEquals(changes[0].b_file_name, "changed_file_name")

    @mock.patch('builtins.open', mock.Mock(return_value=B_FILE_CONTENT))
    def test_that_it_adds_the_magical_a_b_prefix_to_the_paths(self):
        self._diff_list.append(self._diff_mock)
        changes = list(gitmagic.find_changes(self._repo))
        self.assertEquals(changes[0].diff.startswith("--- a/changed_file_name\n+++ b/changed_file_name"), True)

    @mock.patch('builtins.open', mock.Mock(return_value=B_FILE_CONTENT))
    def test_changes_created_lazily(self):
        self._diff_list.append(self._diff_mock)
        self._diff_list_on_second_call.append(self._diff_mock)
        changes_generator = gitmagic.find_changes(self._repo)
        self.assertEqual(self._repo.head.commit.diff.call_count, 0)
        next(changes_generator)
        self.assertEqual(self._repo.head.commit.diff.call_count, 1)
        next(changes_generator)
        self.assertEqual(self._repo.head.commit.diff.call_count, 2)

