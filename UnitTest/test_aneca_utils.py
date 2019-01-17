import unittest
from test_add import *


class Testanecautils(unittest.TestCase):

    def test_author_position(self):
        string = 'Diesel Wolf and Heena Macfarlane and Hashir Marks and Samuel Dunne and Shayla Navarro'
        self.assertEqual(author_position(string, 'Diesel Wolf'), 1)
        self.assertEqual(author_position(string, 'Hashir Marks'), 3)
        self.assertEqual(author_position(string, 'Heena Macfarlane'), 2)

    def test_login(self):
        self.assertEqual(login('asd', 'asd'), True)
        self.assertNotEqual(login(user, pswd), True)

    def test_add_no_idx(self):
        leng = len(db_salida.entries)
        add_no_idx(se2, d, headers, final_url, no_idx_article, 'Tang, Yufei', db_salida, pbar, 1)
        self.assertEqual(leng, len(db_salida.entries))
        add_no_idx(se2, d, headers, final_url, no_idx_article_false, 'Tang, Yufei', db_salida, pbar, 1)
        self.assertNotEqual(leng, len(db_salida.entries))

    def test_add_idx(self):
        leng = len(db_salida.entries)
        add_no_idx(se2, d, headers, final_url, idx_article, 'Tang, Yufei', db_salida, pbar, 1)
        self.assertEqual(leng, len(db_salida.entries))
        add_no_idx(se2, d, headers, final_url, idx_article_false, 'Tang, Yufei', db_salida, pbar, 1)
        self.assertNotEqual(leng, len(db_salida.entries))

    def test_add_book(self):
        leng = len(db_salida.entries)
        add_book(se2, d, headers, final_url, book, 'Aparicio, Virginia', db_salida, pbar, 1)
        self.assertEqual(leng, len(db_salida.entries))
        add_no_idx(se2, d, headers, final_url, book, 'Tang, Yufei', db_salida, pbar, 1)
        self.assertNotEqual(leng, len(db_salida.entries))

    def test_add_inprocedings(self):
        leng = len(db_salida.entries)
        add_inprocedings(se2, d, headers, final_url, inproceedings, db_salida, pbar, 1)
        self.assertEqual(leng, len(db_salida.entries))
        add_no_idx(se2, d, headers, final_url, inproceedings_false, 'Tang, Yufei', db_salida, pbar, 1)
        self.assertNotEqual(leng, len(db_salida.entries))
