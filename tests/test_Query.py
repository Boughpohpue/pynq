# tests/test_pynq.py
import unittest
from pynq.Query import Query

class TestPYNQ(unittest.TestCase):

    def setUp(self):
        self.q = Query([1, 2, 3, 4, 5, 2, 3])
        self.q_group = Query(["apple", "banana", "avocado", "blueberry"])

    # -----------------------------------------------------------
    # Query class wrappers
    # -----------------------------------------------------------
    def test_query_where(self):
        result = self.q.where(lambda x: x % 2 == 0)
        self.assertEqual(result, [2, 4, 2])

    def test_query_select(self):
        result = self.q.select(lambda x: x + 10)
        self.assertEqual(result, [11, 12, 13, 14, 15, 12, 13])

    def test_query_first(self):
        self.assertEqual(self.q.first(lambda x: x > 3), 4)

    def test_query_first_or_default(self):
        self.assertIsNone(self.q.first_or_default(lambda x: x > 10))

    def test_query_last(self):
        self.assertEqual(self.q.last(lambda x: x < 4), 3)

    def test_query_last_or_default(self):
        self.assertIsNone(self.q.last_or_default(lambda x: x > 10))

    def test_query_has(self):
        self.assertTrue(self.q.has(lambda x: x == 5))

    def test_query_count(self):
        self.assertEqual(self.q.count(lambda x: x == 3), 2)

    def test_query_sum(self):
        self.assertEqual(self.q.sum(), 20)
        self.assertEqual(self.q.sum(lambda x: x % 2 == 0), 8)

    def test_query_avg(self):
        self.assertEqual(self.q.avg(), 2.857142857142857)
        self.assertEqual(self.q.avg(lambda x: x > 2), 3.75)

    def test_query_min(self):
        self.assertEqual(self.q.min(), 1)
        self.assertEqual(self.q.min(lambda x: x % 2 == 0), 2)

    def test_query_max(self):
        self.assertEqual(self.q.max(), 5)
        self.assertEqual(self.q.max(lambda x: x % 2 == 0), 4)

    def test_query_order_by(self):
        result = self.q.order_by(lambda x: x)
        self.assertEqual(result, [1, 2, 2, 3, 3, 4, 5])

    def test_query_order_by_desc(self):
        result = self.q.order_by_desc(lambda x: x)
        self.assertEqual(result, [5, 4, 3, 3, 2, 2, 1])

    def test_query_distinct(self):
        result = self.q.distinct()
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_query_take(self):
        result = self.q.take(3)
        self.assertEqual(result, [1, 2, 3])

    def test_query_take_last(self):
        result = self.q.take_last(3)
        self.assertEqual(result, [5, 2, 3])

    def test_query_skip(self):
        result = self.q.skip(2)
        self.assertEqual(result, [3, 4, 5, 2, 3])

    def test_query_skip_last(self):
        result = self.q.skip_last(2)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_group_by(self):
        result = self.q_group.groupBy(lambda x: x[0])
        self.assertEqual(result, [('a', ['apple', 'avocado']), ('b', ['banana', 'blueberry'])])


if __name__ == '__main__':
    unittest.main()
