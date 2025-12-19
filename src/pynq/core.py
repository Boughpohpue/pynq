# pynq/core.py
from typing import Callable, Iterable, Optional
from typing import Any, List, Dict, Tuple, TypeVar
from collections import defaultdict
from itertools import islice


# FOOL OF A ...
T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')


# BASIC

def has_any(seq: Iterable[T]) -> bool:
    try:
        test = seq[0]
        return True
    except:
        return False

def to_list(seq: Iterable[T]) -> List[T]:
    return list(seq)

def has(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> bool:
    return any(predicate(x) if predicate else x for x in seq)

def count(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None) -> int:
    if isinstance(seq, (list, tuple)):
        return len([x for x in seq if x]) if predicate is None else len([x for x in seq if predicate(x)])
    return sum(1 for x in seq if predicate is None or predicate(x))

def sum_of(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, selector: Optional[Callable[[T], K]] = None) -> T:
    return sum(_filter(seq, predicate, selector))

def avg_of(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> float:
    filtered = _filter(seq, predicate, key_selector)
    val = next(filtered, None)
    if not val:
        return val
    items = 0
    total = 0
    while val:
        items += 1
        total += val
        val = next(filtered, None)
    return total / items

def min_of(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, selector: Optional[Callable[[T], K]] = None) -> T:
    filtered = _filter(seq, predicate, selector)
    cur = next(filtered, None)
    if cur:
        for x in filtered:
            if x < cur:
                cur = x
    return cur

def max_of(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, selector: Optional[Callable[[T], K]] = None) -> T:
    filtered = _filter(seq, predicate, selector)
    cur = next(filtered, None)
    if cur:
        for x in filtered:
            if x > cur:
                cur = x
    return cur

def distinct(seq: Iterable[T]) -> Iterable[T]:
    seen = set()
    for item in seq:
        if item not in seen:
            seen.add(item)
            yield item

def contains(seq: Iterable[T], item: T) -> bool:
    return next((True for x in seq if x == item), False)

def contains_all(seq: Iterable[T], items: Iterable[T]) -> bool:
    items_to_find = set(items)
    for x in seq:
        if not items_to_find:
            return True
        items_to_find.discard(x)
    return False

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

def take(seq: Iterable[T], n: int) -> Iterable[T]:
    return islice(seq, n)

def take_last(seq: Iterable[T], n: int) -> Iterable[T]:
    return skip(seq, count(seq) - n)

def skip(seq: Iterable[T], n: int) -> Iterable[T]:
    return islice(seq, n, None)

def skip_last(seq: Iterable[T], n: int) -> Iterable[T]:
    return seq if not n else take(seq, count(seq) - n)


# FILTER & TRANSFORM

def where(seq: Iterable[T], predicate: Callable[[T], bool]) -> Iterable[T]:
    return [x for x in seq if predicate(x)]

def select(seq: Iterable[T], selector: Callable[[T], U]) -> Iterable[U]:
    return (selector(x) for x in seq)

def select_many(seq: Iterable[T], key_selector: Callable[[T], K]) -> Iterable[U]:
    for x in seq:
        yield from key_selector(x)

def with_min(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> Iterable[T]:
    return _with_min_small(seq, predicate, key_selector) if sum(1 for _ in islice(seq, 1269)) < 1269 else _with_min_large(seq, predicate, key_selector)

def with_max(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> Iterable[T]:
    return _with_max_small(seq, predicate, key_selector) if sum(1 for _ in islice(seq, 1269)) < 1269 else _with_max_large(seq, predicate, key_selector)

def order_by(seq: Iterable[T], key_selector: Callable[[T], Any]) -> Iterable[T]:
    return sorted(seq, key=key_selector)

def order_by_desc(seq: Iterable[T], key_selector: Callable[[T], Any]) -> Iterable[T]:
    return sorted(seq, key=key_selector, reverse=True)


# ADVANCED

def group_by(seq: Iterable[T], key_selector: Callable[[T], K], value_selector: Optional[Callable[[T], U]] = None) -> Iterable[Tuple[K, Iterable[U]]]:
    groups: defaultdict[K, list[U]] = defaultdict(list)
    for item in seq:
        key = key_selector(item)
        value = value_selector(item) if value_selector else item
        groups[key].append(value)
    for key, values in groups.items():
        yield key, values

def concatenate(*seqs: Iterable[T]) -> Iterable[T]:
    for seq in seqs:
        for item in seq:
            yield item

def aggregate(seq: Iterable[T], func: Callable[[U, T], U], seed: Optional[U] = None) -> U:
    it = iter(seq)
    if seed is None:
        try:
            seed = next(it)
        except StopIteration:
            raise TypeError("Cannot aggregate empty sequence without seed")
    result: U = seed
    for item in it:
        result = func(result, item)
    return result


# PRIVATE

def _ensure_selector(key_selector: Callable[[T], K]) -> Callable[[T], K]:
    return key_selector if key_selector else lambda value: value

def _filter(seq: Iterable[T], predicate: Callable[[T], bool], key_selector: Callable[[T], K]) -> Iterable[T]:
    key_selector = _ensure_selector(key_selector)
    return (key_selector(x) for x in seq if predicate is None or predicate(key_selector(x)))

def _with_min_large(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> Iterable[T]:
    key_selector = _ensure_selector(key_selector)
    filtered = _filter(seq, predicate)
    cur = next(filtered, None)
    items_with = []
    if cur:
        for x in filtered:
            if key_selector(x) > key_selector(cur):
                continue
            if key_selector(x) < key_selector(cur):
                cur = x
                items_with = []
            items_with.append(cur)
    return items_with

def _with_min_small(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> Iterable[T]:
    key_selector = _ensure_selector(key_selector)
    return _filter(_filter(seq, predicate), lambda x: key_selector(x) == min_of(seq, predicate, key_selector))

def _with_max_large(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> Iterable[T]:
    key_selector = _ensure_selector(key_selector)
    filtered = _filter(seq, predicate)
    cur = next(filtered, None)
    items_with = []
    if cur:
        for x in filtered:
            if key_selector(x) < key_selector(cur):
                continue
            if key_selector(x) > key_selector(cur):
                cur = x
                items_with = []
            items_with.append(cur)
    return items_with

def _with_max_small(seq: Iterable[T], predicate: Optional[Callable[[T], bool]] = None, key_selector: Optional[Callable[[T], K]] = None) -> Iterable[T]:
    key_selector = _ensure_selector(key_selector)
    return _filter(_filter(seq, predicate), lambda x: key_selector(x) == max_of(seq, predicate, key_selector))


if __name__ == '__main__':
    print('Hello PYNQ.core!')
