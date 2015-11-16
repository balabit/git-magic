import gitmagic

def fixup(repo, destination_picker):
    repo.reset()
    for change in gitmagic.find_changes(repo):
        destination_commit = destination_picker.pick(change)
        #todo: apply unified diff from change
        repo.index.commit( message = "fixup! {}".format(destination_commit.message()))

