
from git.cmd import Git


def do_rebase(repo, base_branch, branch_to_rebase=None):
    git = Git(repo.working_dir)
    master = repo.heads['master'].commit
    if branch_to_rebase:
        to_rebase = repo.heads[branch_to_rebase].commit
        repo.heads[branch_to_rebase].checkout()
    else:
        to_rebase = repo.active_branch.commit
    base_branch_commit = repo.heads[base_branch].commit
    # repo.head.reset(commit=base_branch_commit)
    git.execute(['git', 'reset', '--hard', base_branch_commit.hexsha])
    commits_to_pick = [to_rebase]
    for cherry in to_rebase.traverse():
        if cherry == master:
            break
        commits_to_pick.append(cherry)
    for pick in reversed(commits_to_pick):
        git.execute(['git', 'cherry-pick', pick.hexsha])
