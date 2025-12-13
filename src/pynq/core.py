# pynq/core.py
from collections import defaultdict
from collections.abc import Sequence, Iterable as AbcIterable
from typing import Callable, Iterable, TypeVar, List, Dict, Optional, Any
from itertools import islice

T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')

def to_list(seq: Iterable[T]) -> List[T]:
    return list(seq)

def select(seq: Iterable[T], selector: Callable[[T], U]) -> Iterable[U]:
    return (selector(x) for x in seq)

def has(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> bool:
    return any(predicate(x) if predicate else x for x in seq)

def count(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> int:
    if isinstance(seq, (list, tuple)):
        return len([x for x in seq if x]) if predicate is None else len([x for x in seq if predicate(x)])
    return sum(1 for x in seq if predicate is None or predicate(x))

# TODO: Add key selector parameter
def sum_of(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> T:
    return sum(x for x in seq if predicate is None or predicate(x))

# TODO: Add key selector parameter
def avg_of(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> float:
    filtered = [x for x in seq if predicate is None or predicate(x)]
    if len(filtered) == 0:
        raise ValueError("avg_of() arg contains no data after filtering")
    try:
        return sum(filtered) / len(filtered)
    except:
        raise TypeError("avg_of() arg contains items of invalid type")

# TODO: Add key selector parameter
def min_of(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> T:
    filtered = (x for x in seq if predicate is None or predicate(x))
    try:
        cur = next(filtered)
    except StopIteration:
        raise ValueError("min_of() arg contains no data after filtering")
    for x in filtered:
        cur = cur if cur <= x else x
    return cur

# TODO: Add key selector parameter
def max_of(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> T:
    filtered = (x for x in seq if predicate is None or predicate(x))
    try:
        cur = next(filtered)
    except StopIteration:
        raise ValueError("max_of() arg contains no data after filtering")
    for x in filtered:
        cur = cur if cur >= x else x
    return cur

def take(seq: Iterable[T], n: int) -> Iterable[T]:
    return islice(seq, n)

def skip(seq: Iterable[T], n: int) -> Iterable[T]:
    return islice(seq, n, None)

def take_last(seq: Iterable[T], n: int) -> Iterable[T]:
    return skip(seq, count(seq) - n)

def skip_last(seq: Iterable[T], n: int) -> Iterable[T]:
    return seq if not n else take(seq, count(seq) - n)

def where(seq: Iterable[T], predicate: Callable[[T], bool]) -> Iterable[T]:
    return [x for x in seq if predicate(x)]

def first(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> T:
    return seq[0] if not predicate and isinstance(seq, Sequence) else next((x for x in seq if predicate is None or predicate(x)))

def first_or_default(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
    return seq[0] if not predicate and isinstance(seq, Sequence) else next((x for x in seq if predicate is None or predicate(x)), default)

def last(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> T:
    result = None
    for item in seq:
        if predicate is None or predicate(item):
            result = item
    if result is None:
        raise ValueError("No matching element found")
    return result

def last_or_default(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
    result = default
    for item in seq:
        if predicate is None or predicate(item):
            result = item
    return result

def distinct(seq: Iterable[T]) -> Iterable[T]:
    seen = set()
    for item in seq:
        if item not in seen:
            seen.add(item)
            yield item

def order_by(seq: Iterable[T], key_selector: Callable[[T], Any]) -> Iterable[T]:
    return sorted(seq, key=key_selector)

def order_by_desc(seq: Iterable[T], key_selector: Callable[[T], Any]) -> Iterable[T]:
    return sorted(seq, key=key_selector, reverse=True)

def group_by(seq: Iterable[T], key_selector: Callable[[T], K], value_selector: Callable[[T], U] = None) -> Dict[K, List[U]]:
    result = defaultdict(list)
    for item in seq:
        key = key_selector(item)
        value = value_selector(item) if value_selector else item
        result[key].append(value)
    return dict(result)


if __name__ == '__main__':
    print('Hello PYNQ core!')
