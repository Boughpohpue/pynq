# tests/test_pynq.py
import unittest
from pynq.core import (
    to_list,
    sum_of, avg_of,
    min_of, max_of,
    where, distinct,
    has, select,
    count as cnt,
    last, last_or_default,
    first, first_or_default,
    take, take_last,
    skip, skip_last,
    order_by, order_by_desc,
    group_by
)

class TestPYNQ(unittest.TestCase):

    def setUp(self):
        self.data = [1, 2, 3, 4, 5, 2, 3]
        self.group_data = ["apple", "banana", "avocado", "blueberry"]

    # -----------------------------------------------------------
    # Standalone functions
    # -----------------------------------------------------------
    def test_to_list(self):
        self.assertEqual(to_list((x for x in [1, 2, 3])), [1, 2, 3])

    def test_select(self):
        result = list(select(self.data, lambda x: x * 2))
        self.assertEqual(result, [2, 4, 6, 8, 10, 4, 6])

    def test_has(self):
        self.assertTrue(has(self.data, lambda x: x > 4))
        self.assertFalse(has(self.data, lambda x: x > 10))

    def test_count(self):
        self.assertEqual(cnt(self.data), 7)
        self.assertEqual(cnt(self.data, lambda x: x == 2), 2)

    def test_sum_of(self):
        self.assertEqual(sum_of(self.data), 20)
        self.assertEqual(sum_of(self.data, lambda x: x % 2 == 0), 8)

    def test_avg_of(self):
        self.assertEqual(avg_of(self.data), 2.857142857142857)
        self.assertEqual(avg_of(self.data, lambda x: x > 2), 3.75)

    def test_min_of(self):
        self.assertEqual(min_of(self.data), 1)
        self.assertEqual(min_of(self.data, lambda x: x % 2 == 0), 2)

    def test_max_of(self):
        self.assertEqual(max_of(self.data), 5)
        self.assertEqual(max_of(self.data, lambda x: x % 2 == 0), 4)

    def test_take(self):
        result = list(take(self.data, 3))
        self.assertEqual(result, [1, 2, 3])

    def test_skip(self):
        result = list(skip(self.data, 4))
        self.assertEqual(result, [5, 2, 3])

    def test_take_last(self):
        result = list(take_last(self.data, 3))
        self.assertEqual(result, [5, 2, 3])

    def test_skip_last(self):
        result = list(skip_last(self.data, 2))
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_where(self):
        result = where(self.data, lambda x: x % 2 == 0)
        self.assertEqual(result, [2, 4, 2])

    def test_first(self):
        self.assertEqual(first(self.data, lambda x: x > 2), 3)
        self.assertEqual(first(self.data), 1)

    def test_first_or_default(self):
        self.assertEqual(first_or_default(self.data, lambda x: x > 3), 4)
        self.assertIsNone(first_or_default(self.data, lambda x: x > 10))

    def test_last(self):
        self.assertEqual(last(self.data, lambda x: x < 4), 3)
        self.assertEqual(last(self.data), 3)

    def test_last_or_default(self):
        self.assertEqual(last_or_default(self.data, lambda x: x < 3), 2)
        self.assertIsNone(last_or_default(self.data, lambda x: x > 10))

    def test_distinct(self):
        result = list(distinct(self.data))
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_order_by(self):
        result = order_by(self.data, lambda x: x)
        self.assertEqual(result, [1, 2, 2, 3, 3, 4, 5])

    def test_order_by_desc(self):
        result = order_by_desc(self.data, lambda x: x)
        self.assertEqual(result, [5, 4, 3, 3, 2, 2, 1])

    def test_group_by(self):
        result = group_by(self.group_data, lambda x: x[0])
        self.assertEqual(result, {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry']})


if __name__ == '__main__':
    unittest.main()
