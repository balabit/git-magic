from difflib import SequenceMatcher


class Change(object):
    def __init__(self, a_file_name: str, b_file_name: str, a_file_content: str,
                 b_file_content: str, a_hunk: (int, int), b_hunk: (int, int), tag: str):
        self.a_file_name = a_file_name
        self.b_file_name = b_file_name
        self.a_file_content = a_file_content
        self.b_file_content = b_file_content

    def __set__(self, key, value):
        raise TypeError('Immutable class')


def find_changes(repo):
    while True:
        try:
            diff = repo.head.commit.diff(None)[0]
        except IndexError:
            break
        a_file_content = diff.a_blob.data_stream.read().decode()
        b_file_content = diff.b_blob.data_stream.read().decode()
        for tag, a_start, a_end, b_start, b_end in SequenceMatcher(None, a_file_content, b_file_content).get_opcodes():
            if tag == 'equal':
                continue

            yield Change(diff.a_path, diff.b_path, a_file_content, b_file_content,
                         (a_start, a_end), (b_start, b_end), tag)
