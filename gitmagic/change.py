from difflib import SequenceMatcher
from io import StringIO

import git


class Change(object):
    def __init__(self, a_file_name: str, b_file_name: str, a_file_content: [str],
                 b_file_content: [str], a_hunk: (int, int), b_hunk: (int, int), tag: str):
        self.a_file_name = a_file_name
        self.b_file_name = b_file_name
        self.a_file_content = a_file_content
        self.b_file_content = b_file_content
        self.a_hunk = a_hunk
        self.b_hunk = b_hunk
        self.tag = tag

    def unified_diff(self) -> StringIO:
        diff_stream = StringIO()
        diff_stream.write('--- a/{}\n'.format(self.a_file_name))
        diff_stream.write('+++ b/{}\n'.format(self.b_file_name))
        diff_stream.write('@@ -{},{} +{},{} @@\n'.format(self.a_hunk[0], self.a_hunk[1], self.b_hunk[0], self.b_hunk[1]))
        for line in self.a_file_content[max(self.a_hunk[0] - 3, 0):self.a_hunk[0]]:
            diff_stream.write(' {}\n'.format(line))
        for line in self.a_file_content[self.a_hunk[0]:self.a_hunk[1]]:
            diff_stream.write('-{}\n'.format(line))
        for line in self.b_file_content[self.b_hunk[0]:self.b_hunk[1]]:
            diff_stream.write('+{}\n'.format(line))
        for line in self.a_file_content[self.a_hunk[1]:self.a_hunk[1] + 3]:
            diff_stream.write(' {}\n'.format(line))
        diff_stream.seek(0)
        return diff_stream

    def __set__(self, key, value):
        raise TypeError('Immutable class')


def find_changes(repo: git.repo.Repo) -> [Change]:
    while True:
        try:
            diff = repo.head.commit.diff(None)[0]
        except IndexError:
            break
        a_file_content = diff.a_blob.data_stream.read().decode()
        b_file_content = open(diff.b_path).read()
        for tag, a_start, a_end, b_start, b_end in SequenceMatcher(None, a_file_content, b_file_content).get_opcodes():
            if tag == 'equal':
                continue

            yield Change(diff.a_path, diff.b_path, a_file_content, b_file_content,
                         (a_start, a_end), (b_start, b_end), tag)
