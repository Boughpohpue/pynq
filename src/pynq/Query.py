# pynq/Query.py
from collections.abc import Sequence, Iterable as AbcIterable
from typing import Callable, Iterable, TypeVar, List, Optional, Any
from .core import (
    to_list,
    sum_of, avg_of,
    min_of, max_of,
    where, distinct,
    has, select, count,
    last, last_or_default,
    first, first_or_default,
    take, take_last,
    skip, skip_last,
    order_by, order_by_desc,
    group_by
)

T = TypeVar('T')
U = TypeVar('U')
U = TypeVar('K')

class Query(List[T]):
    def where(self, predicate: Callable[[T], bool]) -> 'Query[T]':
        return Query([x for x in self if predicate(x)])

    def select(self, selector: Callable[[T], U]) -> 'Query[U]':
        return Query([selector(x) for x in self])

    def first(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        return first(self, predicate)

    def first_or_default(self, predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
        return first_or_default(self, predicate, default)

    def last(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        return last(self, predicate)

    def last_or_default(self, predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
        return last_or_default(self, predicate, default)

    def has(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        return has(self, predicate)

    def count(self, predicate: Optional[Callable[[T], bool]] = None) -> int:
        return count(self, predicate)

    def sum(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        return sum_of(self, predicate)

    def avg(self, predicate: Optional[Callable[[T], bool]] = None) -> float:
        return avg_of(self, predicate)

    def min(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        return min_of(self, predicate)

    def max(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        return max_of(self, predicate)

    def order_by(self, key_selector: Callable[[T], Any]) -> 'Query[T]':
        return Query(order_by(self, key_selector))

    def order_by_desc(self, key_selector: Callable[[T], Any]) -> 'Query[T]':
        return Query(order_by_desc(self, key_selector))

    def distinct(self) -> 'Query[T]':
        return Query(distinct(self))

    def take(self, n: int) -> 'Query[T]':
        return Query(take(self, n))

    def take_last(self, n: int) -> 'Query[T]':
        return Query(take_last(self, n))

    def skip(self, n: int) -> 'Query[T]':
        return Query(skip(self, n))

    def skip_last(self, n: int) -> 'Query[T]':
        return Query(skip_last(self, n))

    def group_by(self, key_selector: Callable[[T], Any], value_selector: Callable[[T], Any] = None) -> 'Query':
        grouped_dict = group_by(self, key_selector, value_selector)
        return Query((k, v) for k, v in grouped_dict.items())

    # camelCase aliases
    toList = to_list
    takeLast = take_last
    skipLast = skip_last
    firstOrDefault = first_or_default
    lastOrDefault = last_or_default
    orderBy = order_by
    orderByDesc = order_by_desc
    groupBy = group_by


if __name__ == '__main__':
    print('Hello PYNQ Query!')
