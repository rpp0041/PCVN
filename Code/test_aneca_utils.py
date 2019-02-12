import unittest
from test_add import *


class Testanecautils(unittest.TestCase):

    def test_author_position(self):
        # Test if position returned for a author from a list of authors is correct
        string = 'Diesel Wolf and Heena Macfarlane and Hashir Marks and Samuel Dunne and Shayla Navarro'
        self.assertEqual(author_position(string, 'Diesel Wolf'), 1)
        self.assertEqual(author_position(string, 'Hashir Marks'), 3)
        self.assertEqual(author_position(string, 'Heena Macfarlane'), 2)

    def test_login(self):
        # Test if login in ACADEMIA Works
        self.assertEqual(login('asd', 'asd'), True)
        self.assertNotEqual(login(user, pswd), True)

    def test_add_no_idx(self):
        # Test if add no index publications works
        leng = len(db_salida.entries)
        # Wrong publication
        add_no_idx(se2, d, headers, final_url, no_idx_article, 'Tang, Yufei', db_salida, db_completa, pbar, 1, num_var)
        self.assertEqual(leng, len(db_salida.entries))
        # Correct publication
        add_no_idx(se2, d, headers, final_url, no_idx_article_false, 'Tang, Yufei', db_salida, db_completa, pbar, 1, num_var)
        self.assertNotEqual(leng, len(db_salida.entries))

    def test_add_idx(self):
        # Test if add index publications works
        leng = len(db_salida.entries)
        # Wrong publication
        add_no_idx(se2, d, headers, final_url, idx_article, 'Tang, Yufei', db_salida, db_completa, pbar, 1, num_var)
        self.assertEqual(leng, len(db_salida.entries))
        # Correct publication
        add_no_idx(se2, d, headers, final_url, idx_article_false, 'Tang, Yufei', db_salida, db_completa, pbar, 1, num_var)
        self.assertNotEqual(leng, len(db_salida.entries))

    def test_add_book(self):
        # Test if add books works
        leng = len(db_salida.entries)
        add_book(se2, d, headers, final_url, book, 'Aparicio, Virginia', db_salida, db_completa, pbar, 1, num_var)
        self.assertEqual(leng, len(db_salida.entries))
        # Correct publication
        add_no_idx(se2, d, headers, final_url, book, 'Tang, Yufei', db_salida, db_completa, pbar, 1, num_var)
        self.assertNotEqual(leng, len(db_salida.entries))

    def test_add_inprocedings(self):
        # Test if add inbreeding works
        leng = len(db_salida.entries)
        # Wrong publication
        add_inprocedings(se2, d, headers, final_url, inproceedings, db_salida, db_completa, pbar, 1, num_var)
        self.assertEqual(leng, len(db_salida.entries))
        # Correct publication
        add_no_idx(se2, d, headers, final_url, inproceedings_false, 'Tang, Yufei', db_salida, db_completa, pbar, 1, num_var)
        self.assertNotEqual(leng, len(db_salida.entries))
