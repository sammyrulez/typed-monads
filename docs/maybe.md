Undefined values or operations are one particular problem that robust software should prepare for and handle gracefully.

A `Maybe` instance of a certain type `T` will
either be a `Just` object wrapping a value of that type, or `Nothing`.

- Mapping a function over `Nothing` will return `Nothing` without
  calling the function.
- Binding an operation with a `Nothing` will return `Nothing` without
  attempting the operation.


### Default value with _or_else_

Is always nice to have a backup option:

```python

m_empty: Maybe[str] = Nothing()
m_empty.or_else("backup") == "backup"

```

### Differences with _Optional_

The main difference `Maybe` and `Optional` is that you can chain operations without `if guards` statelments.
There is a lot of interoperability between the two types if you want to limit the usage of _Typed Monads_ to your code only.

```python
Just(2) == Maybe.fromOptional(2)
Nothing() == Maybe.fromOptional(None)
2 == Just(2).toOptional()
None == Nothing().toOptional()
```