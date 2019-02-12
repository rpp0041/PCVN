import unittest
from GetPublicationsScholar import *
from test_add import pbar, num_var
import os


class Testgooglescholar(unittest.TestCase):
    def test_parse_abstract(self):
        # Test if remove of extra tags works correctly
        string = ' <div class="gsc_vcd_value" id="gsc_vcd_descr"><div class="gsh_small"><div><div><div class="gsh_csp">Testing parse_abstract </div></div>'
        self.assertEqual(parse_abstract(string), 'Testing parse_abstract ')
        self.assertEqual(parse_abstract('asd'), 'asd')
        self.assertEqual(parse_abstract('<div class="gsh_small">Testing parse_abstract </div>'),
                         'Testing parse_abstract ')
        self.assertRaises(TypeError, parse_abstract, True)
        self.assertRaises(TypeError, parse_abstract, 0)

    def test_parse_google_scholar(self):
        # Extract data from Google Scholar
        get_publications_scholar('ED Schulze', pbar, num_var, 1)
        # Check if data has been correctly saved (file exits)
        self.assertEqual(os.path.isfile('./bibtexScholar.bib'), True)
