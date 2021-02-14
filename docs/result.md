
Represents a state of success or failure, declaring a type for each.
It is the monadic way to error handling.
A `Result` instance will either be an `Ok` object wrapping a value of
the success type `T`, or an `Err` object wrapping a value of the
failure type `E`.

- Mapping a function over an `Err` will return the `Err` unchanged
  without calling the function.
- Binding an operation with an `Err` will return the `Err` unchanged
  without attempting the operation.

```python

m: Result[int, str] = Ok(5)
increment: Callable[[int],int] = lambda x : x +1
Ok(6) == m.map(increment)
e: Result[int, str] = Err("oops")
Err("oops") == e.map(increment) # still an error

```