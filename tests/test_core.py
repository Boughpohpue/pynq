# tests/test_pynq.py
import unittest
from pynq.core import (
    to_list,
    where, distinct,
    sum_of, avg_of,
    min_of, max_of,
    with_min, with_max,
    has, count as cnt,
    select, select_many,
    last, last_or_default,
    first, first_or_default,
    contains, contains_all,
    take, take_last,
    skip, skip_last,
    order_by, order_by_desc,
    aggregate, concatenate,
    group_by
)


class TestPYNQ(unittest.TestCase):

    def setUp(self):
        from .test_data import test_data
        self.empty = test_data["empty"]
        self.strings = test_data["strings"]
        self.integers = test_data["integers"]
        self.dictionary = test_data["dictionary"]
        self.nested_dict = test_data["nested_dict"]


    def test_to_list(self):
        # Arrange:
        expected = list(self.integers)
        # Act:
        result = to_list((x for x in self.integers))
        # Assert:
        self.assertEqual(result, expected)

    def test_has(self):
        self.assertTrue(has(self.integers, lambda x: x > 4))
        self.assertFalse(has(self.integers, lambda x: x > 10))

    def test_count(self):
        # Arrange:
        expected_total = 7
        expected_filtered = 2
        predicate = lambda x: x == 2
        # Act:
        result_total = cnt(self.integers)
        result_filtered = cnt(self.integers, predicate)
        # Assert:
        self.assertEqual(result_total, expected_total)
        self.assertEqual(result_filtered, expected_filtered)

    def test_sum_of(self):
        # Arrange:
        expected_total_sum = 20
        expected_filtered_sum = 8
        filtered_predicate = lambda x: x % 2 == 0
        sum_selector = lambda x: x['year']
        # Act:
        result_total_sum = sum_of(self.integers)
        result_filtered_sum = sum_of(self.integers, filtered_predicate)
        result_dict_sum = sum_of(self.dictionary, lambda x: x <= 40, sum_selector)
        # Assert:
        self.assertEqual(result_total_sum, expected_total_sum)
        self.assertEqual(result_filtered_sum, expected_filtered_sum)
        self.assertEqual(result_dict_sum, 79)

    def test_avg_of(self):
        # Arrange:
        expected_avg = 2.857142857142857
        expected_filtered_avg = 3.75
        filtered_predicate = lambda x: x > 2
        # Act:
        result_avg = avg_of(self.integers)
        result_filtered_avg = avg_of(self.integers, filtered_predicate)
        # Assert:
        self.assertEqual(result_avg, expected_avg)
        self.assertEqual(result_filtered_avg, expected_filtered_avg)

    def test_min_of(self):
        # Arrange:
        expected_min = 1
        expected_filtered_min = 2
        filtered_predicate = lambda x: x % 2 == 0
        # Act:
        result_min = min_of(self.integers)
        result_filtered_min = min_of(self.integers, filtered_predicate)
        # Assert:
        self.assertEqual(result_min, expected_min)
        self.assertEqual(result_filtered_min, expected_filtered_min)

    def test_max_of(self):
        # Arrange:
        expected_max = 5
        expected_filtered_max = 4
        filtered_predicate = lambda x: x % 2 == 0
        # Act:
        result_max = max_of(self.integers)
        result_filtered_max = max_of(self.integers, filtered_predicate)
        # Assert:
        self.assertEqual(result_max, expected_max)
        self.assertEqual(result_filtered_max, expected_filtered_max)

    def test_where(self):
        # Arrange:
        expected_result = [2, 4, 2]
        predicate = lambda x: x % 2 == 0
        # Act:
        result = where(self.integers, predicate)
        # Assert:
        self.assertEqual(result, expected_result)

    def test_distinct(self):
        # Arrange:
        expected_result = [1, 2, 3, 4, 5]
        # Act:
        result = list(distinct(self.integers))
        # Assert:
        self.assertEqual(result, expected_result)

    def test_select(self):
        # Arrange:
        expected_result = [i * 2 for i in self.integers]
        # Act:
        result = list(select(self.integers, lambda x: x * 2))
        # Assert:
        self.assertEqual(result, expected_result)

    def test_select_many(self):
        # Arrange:
        expected_result = []
        selector = lambda x: x["people"]
        for item in self.nested_dict:
            expected_result += selector(item)
        # Act:
        result = list(select_many(self.nested_dict, selector))
        # Assert:
        self.assertEqual(result, expected_result)

    def test_last(self):
        # Arrange:
        expected_result = 3
        predicate = lambda x: x < 4
        # Act:
        result = last(self.integers, predicate)
        # Assert:
        self.assertEqual(result, expected_result)

    def test_last_or_default(self):
        # Arrange:
        expected_result = 2
        predicate = lambda x: x < 3
        expected_default = None
        # Act:
        result = last_or_default(self.integers, predicate)
        result_default = last_or_default(self.integers, lambda x: x > 10)
        # Assert:
        self.assertEqual(result, expected_result)
        self.assertEqual(result_default, expected_default)

    def test_first(self):
        # Arrange:
        expected_result = 3
        predicate = lambda x: x > 2
        # Act:
        result = first(self.integers, predicate)
        # Assert:
        self.assertEqual(result, expected_result)

    def test_first_or_default(self):
        # Arrange:
        expected_result = 4
        predicate = lambda x: x > 3
        expected_default = None
        # Act:
        result = first_or_default(self.integers, predicate)
        result_default = first_or_default(self.integers, lambda x: x > 10)
        # Assert:
        self.assertEqual(result, expected_result)
        self.assertEqual(result_default, expected_default)

    def test_take(self):
        # Arrange:
        count = 3
        expected_result = self.integers[:count]
        # Act:
        result = list(take(self.integers, count))
        # Assert:
        self.assertEqual(result, expected_result)

    def test_take_last(self):
        # Arrange:
        count = 3
        expected_result = self.integers[(len(self.integers) - count):]
        # Act:
        result = list(take_last(self.integers, count))
        # Assert:
        self.assertEqual(result, expected_result)

    def test_skip(self):
        # Arrange:
        count = 4
        expected_result = self.integers[4:]
        # Act:
        result = list(skip(self.integers, count))
        # Assert:
        self.assertEqual(result, expected_result)

    def test_skip_last(self):
        # Arrange:
        count = 2
        expected_result = self.integers[:(count * -1)]
        # Act:
        result = list(skip_last(self.integers, count))
        # Assert:
        self.assertEqual(result, expected_result)

    def test_contains(self):
        # Arrange:
        value_to_check = 4
        value_not_in_list = 10
        # Act:
        result_contains = contains(self.integers, value_to_check)
        result_does_not_contain = contains(self.integers, value_not_in_list)
        # Assert:
        self.assertTrue(result_contains)
        self.assertFalse(result_does_not_contain)

    def test_contains_all(self):
        # Arrange:
        values_to_check = [2, 3]
        values_not_in_list = [2, 10]
        # Act:
        result_contains_all = contains_all(self.integers, values_to_check)
        result_does_not_contain_all = contains_all(self.integers, values_not_in_list)
        # Assert:
        self.assertTrue(result_contains_all)
        self.assertFalse(result_does_not_contain_all)

    def test_order_by(self):
        # Arrange:
        expected_result = [1, 2, 2, 3, 3, 4, 5]
        # Act:
        result = order_by(self.integers, lambda x: x)
        # Assert:
        self.assertEqual(result, expected_result)

    def test_order_by_desc(self):
        # Arrange:
        expected_result = [5, 4, 3, 3, 2, 2, 1]
        # Act:
        result = order_by_desc(self.integers, lambda x: x)
        # Assert:
        self.assertEqual(result, expected_result)

    def test_concatenate(self):
        # Arrange:
        additional_elements = [6, 7, 8]
        expected_result = self.integers + additional_elements
        # Act:
        result = list(concatenate(self.integers, additional_elements))
        # Assert:
        self.assertEqual(result, expected_result)

    def test_aggregate(self):
        # Arrange:
        expected_result = 1
        for x in self.integers:
            expected_result *= x
        aggregate_function = lambda x, y: x * y
        # Act:
        result = aggregate(self.integers, aggregate_function, 1)
        # Assert:
        self.assertEqual(result, expected_result)

    def test_group_by(self):
        from .test_data import get_strings_grouped_by
        # Arrange:
        selector = lambda x: x[0]
        expected_result = get_strings_grouped_by(selector)
        # Act:
        result = list(group_by(self.strings, selector))
        # Assert:
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
