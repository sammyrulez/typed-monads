
 Applicative functors, or an applicative for short, allow for functorial computations to be sequenced (unlike plain functors), but don't allow using results from prior computations in the definition of subsequent ones (unlike monads). Applicative functors are the programming equivalent of lax monoidal functors with tensorial strength in category theory.

*Extends `Functor`.*

#### pure

Wraps a value in an applicative functor.

e.g.:

    Maybe.pure("abc") == Just("abc")
    Result.pure(123) == Ok(123)

#### apply (`&`)

Transforms the value contained in the instance's functor with a
function wrapped in the same type of functor.

The `&` operator implements apply on applicatives, and is
right-associative.

e.g.:

```python
increment = lambda x: x + 1

Just(3).apply(Just(increment)) == Just(increment) & Just(3) == Just(4)
```

This can be very handily combined with map to apply curried functions
to multiple arguments:

```python
subtract = lambda x: lambda y: x - y

subtract * Just(10) & Just(4) == Just(6)
```