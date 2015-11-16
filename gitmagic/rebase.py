
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


def do_fixup(repo, fixup_into, commit_to_fixup):
    git = Git(repo.working_dir)

    commits_to_pick = []
    if commit_to_fixup != repo.head.commit:
        commits_to_pick.append(repo.head.commit)
    for cherry in repo.head.commit.traverse():
        if cherry == fixup_into:
            break
        if cherry == commit_to_fixup:
            continue
        commits_to_pick.append(cherry)
    git.execute(['git', 'reset', '--hard', fixup_into.hexsha])
    git.execute(['git', 'cherry-pick', commit_to_fixup.hexsha])
    git.execute(['git', 'reset', '--soft', 'HEAD~1'])
    git.execute(['git', 'commit', '--amend', '--no-edit'])
    for pick in reversed(commits_to_pick):
        git.execute(['git', 'cherry-pick', pick.hexsha])
