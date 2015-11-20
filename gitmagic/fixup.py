# Copyright (c) 2015 BalaBit
# All rights reserved.

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
        gitmagic.checkpoint( _colorize_change(change, destination), args)
        repo.index.commit( message = "fixup! {}".format(destination.message))

def _apply_change(repo, change):
    file_name = ""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(change.diff)
        file_name = f.name

    git_ = git.cmd.Git(repo.working_dir)
    git_.execute(['git', 'apply', '--cache', file_name])

NO_COLOR = "\033[0m"
YELLOW = "\033[1;33m"
WHITE = "\033[1;37m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
BLUE = "\033[1;36m"

def _colorize(message, color):
    return "{}{}{}".format(color, message, NO_COLOR)

def _colorize_change(change, commit):
    message = _colorize("Should I create fixup commit for {} -> {}:{}\n".format(
            change.a_file_name,
            commit.hexsha[:7],
            commit.summary), YELLOW)
    message += _diff_colorizer(change.diff)
    return message

def _is_diff_header_line(line):
    return line[:1] == "@" or line[:3] == "+++" or line[:3] == "---"

def _diff_colorizer(diff):
    colorized = ""
    for line in diff.splitlines(keepends=True):
        color = WHITE
        first_char = line[:1]
        if first_char == "-":
            color = RED
        if first_char == "+":
            color = GREEN
        if _is_diff_header_line(line):
            color = BLUE
        colorized += _colorize(line, color)
    return colorized
