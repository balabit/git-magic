import gitmagic

def fixup(repo):
    repo.reset()
    for change in gitmagic.find_changes(repo):
        pass

