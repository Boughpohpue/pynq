# pynq/pynquery.py
from .core import (
    has_any, to_list, has, count, sum_of, avg_of, min_of, max_of,
    distinct, contains, contains_all, first, first_or_default, last,
    last_or_default, take, take_last, skip, skip_last, where, select,
    select_many, with_min, with_max, order_by, order_by_desc, group_by,
    aggregate, concatenate
)
from .pyngrouping import PynGrouping
from typing import Generic, Callable, Iterable, Optional
from typing import Any, List, Union, Iterator, TypeVar


# FOOL OF A ...
T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')


class PynQuery(Generic[T]):

    def __init__(self, iterable: Iterable[T]):
        self._iterable = iterable

    def __iter__(self):
        return iter(self._iterable)

    def __hash__(self) -> int:
        return hash(tuple(self._iterable))

    def __eq__(self, other: object) -> bool:
        return self.equals(other)

    def equals(self, other: Union['PynQuery[T]', Iterable[T]]) -> bool:
        if isinstance(other, PynQuery):
            other_iterable = other._iterable
        elif isinstance(other, Iterable):
            other_iterable = other
        else:
            return False
        return list(self._iterable) == list(other_iterable)

    # BASIC

    def all(self) -> Iterable[T]:
        return self._iterable

    def any(self) -> bool:
        return has_any(self._iterable)

    def to_list(self) -> List[T]:
        return to_list(self._iterable)

    def has(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        return has(self._iterable, predicate)

    def count(self, predicate: Optional[Callable[[T], bool]] = None) -> int:
        return count(self._iterable, predicate)

    def sum(self, predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> T:
        return sum_of(self._iterable, predicate, key_selector)

    def avg(self, predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> float:
        return avg_of(self._iterable, predicate, key_selector)

    def min(self, predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> T:
        return min_of(self._iterable, predicate, key_selector)

    def max(self, predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> T:
        return max_of(self._iterable, predicate, key_selector)

    def distinct(self) -> 'PynQuery[T]':
        return PynQuery(distinct(self._iterable))

    def contains(self, item: T) -> bool:
        return contains(self._iterable, item)

    def contains_all(self, items: Iterable[T]) -> bool:
        return contains_all(self._iterable, items)

    def first(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        return first(self._iterable, predicate)

    def first_or_default(self, predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
        return first_or_default(self._iterable, predicate, default)

    def last(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        return last(self._iterable, predicate)

    def last_or_default(self, predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
        return last_or_default(self._iterable, predicate, default)

    def take(self, n: int) -> 'PynQuery[T]':
        return PynQuery(take(self._iterable, n))

    def take_last(self, n: int) -> 'PynQuery[T]':
        return PynQuery(take_last(self._iterable, n))

    def skip(self, n: int) -> 'PynQuery[T]':
        return PynQuery(skip(self._iterable, n))

    def skip_last(self, n: int) -> 'PynQuery[T]':
        return PynQuery(skip_last(self._iterable, n))

    # FILTER & TRANSFORM

    def where(self, predicate: Callable[[T], bool]) -> 'PynQuery[T]':
        return PynQuery(where(self._iterable, predicate))

    def select(self, selector: Callable[[T], U]) -> 'PynQuery[U]':
        return PynQuery(select(self._iterable, selector))

    def select_many(self, key_selector: Callable[[T], Iterable[U]]) -> 'PynQuery[U]':
        return PynQuery(select_many(self._iterable, key_selector))

    def with_min(self, predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> 'PynQuery[T]':
        return PynQuery(with_min(self._iterable, predicate, key_selector))

    def with_max(self, predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> 'PynQuery[T]':
        return PynQuery(with_max(self._iterable, predicate, key_selector))


    # ADVANCED

    def order_by(self, key_selector: Callable[[T], Any]) -> 'PynQuery[T]':
        return PynQuery(order_by(self._iterable, key_selector))

    def order_by_desc(self, key_selector: Callable[[T], Any]) -> 'PynQuery[T]':
        return PynQuery(order_by_desc(self._iterable, key_selector))

    def group_by(self, key_selector: Callable[[T], K], value_selector: Optional[Callable[[T], U]] = None) -> 'PynQuery[PynGrouping[K, U]]':
        return PynQuery(
            PynGrouping(k, v)
            for k, v in group_by(self._iterable, key_selector, value_selector)
        )

    def aggregate(self, func: Callable[[U, T], U], seed: Optional[U] = None) -> U:
        return aggregate(self._iterable, func, seed)

    def concatenate(self, *seqs: Iterable[T]) -> Iterable[T]:
        return concatenate(self._iterable, seqs)


    # ALIASES
    toList = to_list
    withMin = with_min
    withMax = with_max
    takeLast = take_last
    skipLast = skip_last
    selectMany = select_many
    containsAll = contains_all
    firstOrDefault = first_or_default
    lastOrDefault = last_or_default
    orderByDesc = order_by_desc
    orderBy = order_by
    groupBy = group_by


if __name__ == '__main__':
    print('Hello PYNQ.PynQuery!')
