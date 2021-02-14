

A monad is an abstraction that allows structuring programs generically. Monads achieve this by providing their own data type (a particular type for each type of monad), which represents a specific form of computation, along with one procedure to wrap values of any basic type within the monad (yielding a monadic value) and another to compose functions that output monadic values (called monadic functions).
This allows monads to simplify a wide range of problems, like handling potential undefined values (with the Maybe monad), or keeping values within a flexible, well-formed list (using the List monad). With a monad, a programmer can turn a complicated sequence of functions into a succinct pipeline that abstracts away auxiliary data management, control flow, or side-effects.


*Extends `Applicative`.*

#### bind (`>>`)

Passes the value within the monad through an operation returning the
same type of monad, allowing multiple operations to be chained.

The `>>` operator implements bind on monads, and is left-associative.

```python
@curry
def lookup(key: str, dictionary: Dict[str, str]) -> Maybe[str]:
    try:
        return Just(dictionary[key])
    except KeyError:
        return Nothing()


result = Just({"hello": "world"}).bind(lookup("hello")).bind(lambda s: s.upper())
result = (
    Just({"hello": "world"})
    >> lookup("hello")
    >> (lambda s: s.upper())
)
```