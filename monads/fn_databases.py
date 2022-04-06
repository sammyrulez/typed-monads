try:
    from databases import Database  # type: ignore
except ImportError:
    print(
        "This module needs sqlalchemy and databases deps. installed. please install :\n pip install databases"
    )

from typing import Awaitable, Callable, Iterable, List, TypeVar, Union

from .future import Future
from .monad import Monad

T = TypeVar("T")
S = TypeVar("S")


class Query(Monad[T]):
    def __init__(self, database: Database, query: str) -> None:
        self.database = database
        self.query = query

    @classmethod
    def pure(cls, database: Database, query: str) -> Monad[T]:
        return Query(database, query)

    def map(self, function: Callable[[T], S]) -> Future[List[S]]:
        f_q = self.database.fetch_all(query=self.query)
        
        f_m = Future(f_q).map(function)
        return f_m


