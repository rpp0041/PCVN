import unittest
from GetPublicationsWOS import *
from test_add import pbar
import os


class Testwos(unittest.TestCase):
    def test_wos(self):
        # Extract data from Web of Sciece
        get_publications_wos('ASD', pbar)
        # Check if data has been correctly saved (file exits)
        self.assertEqual(os.path.isfile('./savedrecs.bib'), True)

