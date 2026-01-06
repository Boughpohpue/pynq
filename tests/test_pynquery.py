# tests/test_PynQuery.py
import unittest
from pynq.pynquery import PynQuery
from .test_data import test_data
from .test_data import get_integers_avg, get_integers_avg_with_predicate, get_strings_grouped_by

class TestPYNQ(unittest.TestCase):

    def setUp(self):
        self.empty = PynQuery(test_data["empty"])
        self.strings = PynQuery(test_data["strings"])
        self.integers = PynQuery(test_data["integers"])
        self.dictionary = PynQuery(test_data["dictionary"])
        self.nested_dict = PynQuery(test_data["nested_dict"])

    def test_pynquery_any_with_items(self):
        # Arrange:
        expected = True
        # Act:
        result = self.integers.any()
        # Assert
        self.assertEqual(result, expected)

    def test_pynquery_any_with_no_items(self):
        # Arrange:
        expected = False
        # Act:
        result = self.empty.any()
        # Assert
        self.assertEqual(result, expected)

    def test_pynquery_toList(self):
        # Arrange:
        expected = list(self.integers)
        # Act:
        result = self.integers.toList()
        # Assert
        self.assertEqual(result, expected)

    def test_pynquery_select(self):
        # Arrange:
        expected = []
        selector = lambda x: x + 10
        for x in self.integers:
            expected.append(selector(x))
        # Act:
        result = list(self.integers.select(selector))
        # Assert
        self.assertEqual(result, expected)

    def test_pynquery_selectMany(self):
        # Arrange:
        expected = []
        selector = lambda x: x["people"]
        for x in self.nested_dict:
            expected += selector(x)
        # Act:
        result = list(self.nested_dict.selectMany(selector))
        # Assert
        self.assertEqual(result, expected)

    def test_pynquery_where(self):
        result = self.integers.where(lambda x: x % 2 == 0)
        self.assertEqual(result, [2, 4, 2])

    def test_pynquery_select(self):
        result = self.integers.select(lambda x: x + 10)
        self.assertEqual(result, [11, 12, 13, 14, 15, 12, 13])

    def test_pynquery_first(self):
        self.assertEqual(self.integers.first(lambda x: x > 3), 4)

    def test_pynquery_first_or_default(self):
        self.assertIsNone(self.integers.first_or_default(lambda x: x > 10))

    def test_pynquery_last(self):
        self.assertEqual(self.integers.last(lambda x: x < 4), 3)

    def test_pynquery_last_or_default(self):
        self.assertIsNone(self.integers.last_or_default(lambda x: x > 10))

    def test_pynquery_has(self):
        self.assertTrue(self.integers.has(lambda x: x == 5))

    def test_pynquery_count(self):
        self.assertEqual(self.integers.count(lambda x: x == 3), 2)

    def test_pynquery_sum(self):
        self.assertEqual(self.integers.sum(), 20)
        self.assertEqual(self.integers.sum(lambda x: x % 2 == 0), 8)

    def test_pynquery_avg(self):
        self.assertEqual(self.integers.avg(), get_integers_avg())
        self.assertEqual(self.integers.avg(lambda x: x > 2), get_integers_avg_with_predicate(lambda x: x > 2))

    def test_pynquery_min(self):
        self.assertEqual(self.integers.min(), 1)
        self.assertEqual(self.integers.min(lambda x: x % 2 == 0), 2)

    def test_pynquery_max(self):
        self.assertEqual(self.integers.max(), 5)
        self.assertEqual(self.integers.max(lambda x: x % 2 == 0), 4)

    def test_pynquery_order_by(self):
        result = self.integers.order_by(lambda x: x)
        self.assertEqual(result, [1, 2, 2, 3, 3, 4, 5])

    def test_pynquery_order_by_desc(self):
        result = self.integers.order_by_desc(lambda x: x)
        self.assertEqual(result, [5, 4, 3, 3, 2, 2, 1])

    def test_pynquery_distinct(self):
        result = self.integers.distinct()
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_pynquery_take(self):
        result = self.integers.take(3)
        self.assertEqual(result, [1, 2, 3])

    def test_pynquery_take_last(self):
        result = self.integers.take_last(3)
        self.assertEqual(result, [5, 2, 3])

    def test_pynquery_skip(self):
        result = self.integers.skip(2)
        self.assertEqual(result, [3, 4, 5, 2, 3])

    def test_pynquery_skip_last(self):
        result = self.integers.skip_last(2)
        self.assertEqual(result, [1, 2, 3, 4, 5])

'''
    def test_group_by(self):
        # Arrange:
        selector = lambda x: x[0]
        expected_result = get_strings_grouped_by(selector)
        # Act:
        result = list(self.strings.group_by(selector))
        # Assert:
        self.assertEqual(result, expected_result)
'''


if __name__ == '__main__':
    unittest.main()
