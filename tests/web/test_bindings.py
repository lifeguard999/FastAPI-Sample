import unittest
import lib.db
import web.bindings


class TestBindings(unittest.TestCase):

    def setUp(self):
        lib.db.init()

    def test_find_title_by_id(self):
        data = web.bindings.find_title_by_id(1)
        self.assertEqual(len(data), 4)

    def test_find_titles(self):
        data = web.bindings.find_titles('freehold', 'id', 'desc', 1, 10)
        self.assertEqual(10, len(data))
        self.assertEqual(999, data[0]['id'])
