import unittest
from GroupFilesUtils import *


class Testgroupfilesutils(unittest.TestCase):

    def test_check_issn(self):
        dic1 = {'issn': '1234567'}
        dic2 = {'issn': '1234567'}
        dic3 = {'issn': '1594786'}
        dic4 = {'author': 'author_test'}
        self.assertEqual(check_issn(dic1, dic2), True)
        self.assertEqual(check_issn(dic1, dic3), False)
        self.assertEqual(check_issn(dic2, dic3), False)
        self.assertEqual(check_issn(dic1, dic4), False)

    def test_check_title(self):
        dic1 = {'title': 'test_title'}
        dic2 = {'title': 'testtitle'}
        dic3 = {'title': 'this title is not equal'}
        dic4 = {'author': 'author_test'}
        self.assertEqual(check_title(dic1, dic2), True)
        self.assertEqual(check_title(dic1, dic3), False)
        self.assertEqual(check_title(dic2, dic3), False)
        self.assertEqual(check_title(dic1, dic4), False)

    def test_remove_duplicates(self):
        dic1 = {'issn': '1234567', 'title': 'test_title'}
        dic2 = {'issn': '1234567', 'title': 'this title is not equal'}
        dic3 = {'issn': '1594786', 'title': 'test_title'}
        dic4 = {'author': 'author_test'}
        l1 = list()
        l1.extend([dic1, dic4])
        l2 = list()
        l2.extend([dic2, dic3])
        list1 = l1.copy()
        l1, l2 = remove_duplicates(l1, l2)
        self.assertNotEqual(l1, list1)

    def test_parse_volume(self):
        dic1 = {'volume': '7906 LNAI', 'title': 'test_title'}
        dic2 = {'volume': '1234567', 'title': 'this title is not equal'}
        dic3 = {'volume': '1', 'title': 'test_title'}

        pub = parse_volume(dic1)
        pub2 = parse_volume(dic2)
        pub3 = parse_volume(dic3)
        self.assertEqual(pub['volume'], '7906')
        self.assertEqual(pub2['volume'], '1234567')
        self.assertEqual(pub3['volume'], '1')

    def test_parse_impact_index(self):
        dic1 = {'impactIndex': 5}
        dic2 = {'impactIndex': '5'}
        dic3 = {'impactIndex': '0'}

        self.assertEqual('impactIndex' in parse_impact_index(dic1), True)
        self.assertEqual('impactIndex' in parse_impact_index(dic2), True)
        self.assertEqual('impactIndex' in parse_impact_index(dic3), False)

    def test_parse_string(self):
        str1 = 'asd___ this is a test'
        str2 = 'asd--- %THi$s is a T_e_sT'
        str3 = 'asd  %7            this          is a   t e s t'

        self.assertEqual(parse_string(str1), parse_string(str2))
        self.assertEqual(parse_string(str1), parse_string(str3))
        self.assertEqual(parse_string(str2), parse_string(str3))

    def test_calculate_tertile(self):
        rank1 = '1/20'
        rank2 = '50/50'
        rank3 = 100
        rank4 = True

        self.assertEqual(calculate_tertile(rank1), 1)
        self.assertEqual(calculate_tertile(rank2), 3)
        self.assertEqual(calculate_tertile(rank3), 'None')
        self.assertEqual(calculate_tertile(rank4), 'None')
