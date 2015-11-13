import unittest
import gitmagic

class TestFixupDestinationPicker(unittest.TestCase):
    def test_that_it_is_instantiable(self):
        repo=0
        commit_range=0
        gitmagic.FixupDestinationPicker(repo, commit_range)

