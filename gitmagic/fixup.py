import gitmagic


def fixup(repo, destination_picker, change_finder, args={}):
    repo.index.reset()
    for change in change_finder(repo):
        _apply_change(repo, change)
        destination_commit = destination_picker.pick(change)
        gitmagic.checkpoint("Should I create fixup commit for {} -> {}:{}".format(
            change.a_file_name,
            destination_commit.hexsha[:7],
            destination_commit.summary,
            ), args)
        repo.index.commit( message = "fixup! {}".format(destination_commit.message))

def _apply_change(repo, change):
    #todo: apply unified diff only
    repo.index.add([change.a_file_name])

