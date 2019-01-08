import unittest
from GetPublicationsScholar import parse_abstract

class test_google_scholar(unittest.TestCase):
	def test_parse_abstract(self):
		string = ' <div class="gsc_vcd_value" id="gsc_vcd_descr"><div class="gsh_small"><div><div><div class="gsh_csp">Testing parse_abstract </div></div>'
		self.assertEqual(parse_abstract(string),'Testing parse_abstract ')
		self.assertEqual(parse_abstract('asd'),'asd')
		self.assertEqual(parse_abstract('<div class="gsh_small">Testing parse_abstract </div>'),'Testing parse_abstract ')
		self.assertRaises(TypeError,parse_abstract,True)
		self.assertRaises(TypeError,parse_abstract,0)
