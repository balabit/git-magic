import gitmagic

def fixup(repo, destination_picker):
    repo.reset()
    for change in gitmagic.find_changes(repo):
        destination_picker.pick(change)

