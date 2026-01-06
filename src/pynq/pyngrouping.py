# pynq/pyngrouping.py
from typing import Generic, Iterable
from typing import List, Tuple, Iterator, TypeVar
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pynquery import PynQuery


U = TypeVar('U')
K = TypeVar('K')


class PynGrouping(Generic[K, U], Iterable[U]):

    def __init__(self, key: K, values: Iterable[U]):
        self.key = key
        self._values = values

    def __iter__(self) -> Iterator[U]:
        return iter(self._values)

    def as_queryable(self) -> 'PynQuery[U]':
        from .pynquery import PynQuery
        return PynQuery(self)

    def as_tuple(self) -> Tuple[K, List[U]]:
        return (self.key, self._values)

    asQueryable = as_queryable


if __name__ == '__main__':
    print('Hello PYNQ.PynGrouping!')
