import unittest
import lib.utils as utils


class TestUtils(unittest.TestCase):

    def test_memoize_noargs(self):
        counter = [0]
        @utils.memoize
        def test_func():
            counter[0] += 1
            return 1
        self.assertEqual(1, test_func())
        self.assertEqual(1, test_func())
        self.assertEqual(1, counter[0])

    def test_memoize_args(self):
        counter = [0]
        @utils.memoize
        def test_func(x):
            counter[0] += 1
            return x
        self.assertEqual(1, test_func(1))
        self.assertEqual(1, test_func(1))
        self.assertEqual(2, test_func(2))
        self.assertEqual(2, test_func(2))
        self.assertEqual(2, counter[0])

    def test_get_project_path(self):
        path = utils.get_project_path()
        self.assertIsInstance(path, str)
        self.assertGreater(len(path), 5)

    def test_pad_list_right(self):
        lst = [1, ]
        utils.pad_list_right(lst, 0, 3)
        self.assertEqual([1, 0, 0], lst)
        lst = [1, 1, 1]
        utils.pad_list_right(lst, 0, 3)
        self.assertEqual([1, 1, 1], lst)
        lst = [1, 1, 1, 1]
        utils.pad_list_right(lst, 0, 3)
        self.assertEqual([1, 1, 1, 1], lst)
