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
    def test_that_it_returns_the_list_of_changes(self):
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
    def test_changes_created_lazily(self):
        self._diff_list.append(self._diff_mock)
        self._diff_list_on_second_call.append(self._diff_mock)
        changes_generator = gitmagic.find_changes(self._repo)
        self.assertEqual(self._repo.head.commit.diff.call_count, 0)
        next(changes_generator)
        self.assertEqual(self._repo.head.commit.diff.call_count, 1)
        next(changes_generator)
        self.assertEqual(self._repo.head.commit.diff.call_count, 2)


class TestChange(unittest.TestCase):
    def setUp(self):
        orig = ['line0', 'line1', 'line2', 'line3',
                'line4', 'line5', 'line6', 'line7']
        new = ['newline'] + orig[:-1]
        new[4] = 'replaced_line'
        self.replace_unified_diff = gitmagic.Change(
            'file1', 'file2', orig, new,
            (3, 4), (4, 5), 'replace'
        ).diff

    def test_change_unified_diff_contains_filename(self):
        self.assertIn('--- a/file1', self.replace_unified_diff)
        self.assertIn('+++ b/file2', self.replace_unified_diff)

    def test_change_unified_diff_contains_the_replace_diff(self):
        self.assertIn('-line3', self.replace_unified_diff)
        self.assertIn('+replaced_line', self.replace_unified_diff)

    def test_diff_contains_the_context(self):
        self.assertIn(' line0', self.replace_unified_diff)
        self.assertIn(' line5', self.replace_unified_diff)

    def test_diff_contains_the_line_numbers(self):
        self.assertIn(
            '@@ -{},{} +{},{} @@'.format(
                3, 4,
                4, 5),
            self.replace_unified_diff
        )

    def test_diff_has_right_length(self):
        lines = self.replace_unified_diff.rstrip('\n').split('\n')
        header = 2
        diffstat = 1
        context = 6
        deletions = 1
        insertions = 1
        self.assertEqual(len(lines),
                         header + context + diffstat +
                         deletions + insertions)
