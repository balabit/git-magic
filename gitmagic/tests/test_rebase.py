import unittest
from gitmagic.rebase import do_rebase
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
