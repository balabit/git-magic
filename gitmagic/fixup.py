import gitmagic


def fixup(repo, destination_picker):
    repo.reset()
    for change in gitmagic.find_changes(repo):
        _apply_change(repo, change)
        destination_commit = destination_picker.pick(change)
        repo.index.commit( message = "fixup! {}".format(destination_commit.message()))

def _apply_change(repo, change):
    #todo: apply unified diff only
    repo.index.add(change.file_name)

