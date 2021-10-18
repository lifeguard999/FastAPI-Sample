import unittest
import lib.db


class TestDb(unittest.TestCase):

    def setUp(self):
        lib.db.init()

    def test_get_titles_list(self):
        data = lib.db._load_titles()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 7)
        self.assertIsInstance(data[0], dict)
        self.assertIn('id', data[0])
        self.assertIsInstance(data[0]['id'], int)
        self.assertIn('title_number', data[0])
        self.assertIsInstance(data[0]['title_number'], str)
        self.assertIn('title_class', data[0])
        self.assertIsInstance(data[0]['title_class'], str)

    def test_filter_data(self):
        f = lib.db.filter_data(lib.db.TITLES_DATA, 'freehold')
        l = lib.db.filter_data(lib.db.TITLES_DATA, 'leasehold')
        x = lib.db.filter_data(lib.db.TITLES_DATA, 'bla')
        self.assertEqual(len(x), 0)
        self.assertGreater(len(f), 0)
        self.assertGreater(len(l), 0)
        self.assertEqual(len(l) + len(f), len(lib.db.TITLES_DATA))

    def test_sort_data(self):
        s = lib.db.sort_data(lib.db.TITLES_DATA, 'id', '')
        self.assertEqual(len(s), len(lib.db.TITLES_DATA))
        self.assertEqual(s[0]['id'], 0)
        s = lib.db.sort_data(lib.db.TITLES_DATA, 'id', 'desc')
        self.assertEqual(s[0]['id'], 999)
        s = lib.db.sort_data(lib.db.TITLES_DATA, 'title_number,id', 'desc, desc')
        self.assertEqual(s[0]['title_number'], 'ZW841')
        s = lib.db.sort_data(lib.db.TITLES_DATA, 'title_number,id', 'asc')
        self.assertEqual(s[0]['title_number'], 'AAQC760254')

    def test_paginate_data(self):
        data = list(range(101))
        s = lib.db.paginate_data(data, 0, 10)
        self.assertEqual(len(data), len(s))
        s = lib.db.paginate_data(data, 1, 0)
        self.assertEqual(len(data), len(s))
        s = lib.db.paginate_data(data, 1, 10)
        self.assertEqual(list(range(0, 10)), s)
        s = lib.db.paginate_data(data, 3, 10)
        self.assertEqual(list(range(20, 30)), s)
        s = lib.db.paginate_data(data, 11, 10)
        self.assertEqual([100], s)
        s = lib.db.paginate_data(data, 12, 10)
        self.assertEqual([], s)
