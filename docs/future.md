Represents an asynchronous action.


```python

# Lazy values and operations
mapped_future: Future[int] = Future.pure(1).map(lambda x: x + 1)
await mapped_future

# convert sync calls in  async
f: Callable[[int], int] = lambda x: x + 1
await Future.pure(3).map(f) == await Future.pure(3).apply(Future.pure(f))

```

- Also implements `Awaitable`.