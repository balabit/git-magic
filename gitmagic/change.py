import difflib
from io import StringIO

import git


class Change(object):
    def __init__(self, a_file_name: str, b_file_name: str, a_file_content: [str],
                 b_file_content: [str], a_hunk: (int, int), b_hunk: (int, int), diff: str):
        self.a_file_name = a_file_name
        self.b_file_name = b_file_name
        self.a_file_content = a_file_content
        self.b_file_content = b_file_content
        self.a_hunk = a_hunk
        self.b_hunk = b_hunk
        self.diff = diff

    def __set__(self, key, value):
        raise TypeError('Immutable class')


def find_changes(repo: git.repo.Repo) -> [Change]:
    while True:
        try:
            diff = repo.head.commit.diff(None)[0]
        except IndexError:
            break
        a_file_content = [ x + "\n" for x in diff.a_blob.data_stream.read().decode().split('\n') ]
        b_file_content = [ x + "\n" for x in open(diff.b_path).read().split('\n') ]
        for tag, a_start, a_end, b_start, b_end in difflib.SequenceMatcher(None, a_file_content, b_file_content).get_opcodes():
            if tag == 'equal':
                continue

            unified_diff = ""
            for line in difflib.unified_diff(a_file_content[:a_end + 3],b_file_content[:b_end + 3], fromfile=diff.a_path, tofile=diff.b_path):
                unified_diff+=line
                if line[-1]!="\n":
                    unified_diff+="\n"

            yield Change(diff.a_path, diff.b_path, a_file_content, b_file_content,
                         (a_start, a_end), (b_start, b_end), unified_diff)
            break
