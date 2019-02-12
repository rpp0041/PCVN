import unittest
from GetPublicationsScopus import *
from test_add import pbar
import os


class Testscopus(unittest.TestCase):
    def test_scopus(self):
        # Extract data from Scopus
        get_publications_scopus('56512368400', pbar)
        # Check if data has been correctly saved (file exits)
        self.assertEqual(os.path.isfile('./scopus.bib'), True)

