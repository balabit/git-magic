import gitmagic


def fixup(repo, destination_picker, change_finder):
    repo.index.reset()
    for change in change_finder(repo):
        _apply_change(repo, change)
        destination_commit = destination_picker.pick(change)
        repo.index.commit( message = "fixup! {}".format(destination_commit.message))

def _apply_change(repo, change):
    #todo: apply unified diff only
    repo.index.add([change.a_file_name])

