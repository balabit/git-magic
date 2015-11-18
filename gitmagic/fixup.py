import gitmagic
import git.cmd
import tempfile

def fixup(repo, destination_picker, change_finder, args={}):
    repo.index.reset()
    for change in change_finder(repo):
        _apply_change(repo, change)
        destination_commits = destination_picker.pick(change)
        if not destination_commits:
            repo.index.commit( message = "WARNING: no destination commit")
            continue

        destination = destination_commits[0]
        gitmagic.checkpoint("Should I create fixup commit for {} -> {}:{}\n{}".format(
            change.a_file_name,
            destination.hexsha[:7],
            destination.summary,
            change.diff), args)
        repo.index.commit( message = "fixup! {}".format(destination.message))

def _apply_change(repo, change):
    file_name = ""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(change.diff)
        file_name = f.name

    git_ = git.cmd.Git(repo.working_dir)
    git_.execute(['git', 'apply', '--cache', file_name])

