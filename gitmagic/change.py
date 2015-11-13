from collections import namedtuple
Change = namedtuple("Change", ["file_name"])


def find_changes(repo):
    for diff in repo.head.commit.diff(None):
        yield Change(diff.a_path)

