import unittest
from gitmagic.rebase import do_rebase, do_fixup
from git import Repo
import pickle


class TestRebase(unittest.TestCase):
    def setUp(self):
        # with open('gitmagic/tests/testrepo.pickle') as testrepo_file:
        #     pickled_repo = testrepo_file.readline()
        #     self._repo = pickle.loads(pickled_repo)
        self._repo = Repo('gitmagic/tests/testrepo/')

    # def test_rebase(self):
    #     do_rebase(self._repo, 'new_master', 'new_branch')

    def test_fixup(self):
        fixup_into = self._repo.head.commit.parents[0].parents[0].parents[0]
        commit_to_fixup = self._repo.head.commit.parents[0]
        do_fixup(self._repo, fixup_into, commit_to_fixup)
