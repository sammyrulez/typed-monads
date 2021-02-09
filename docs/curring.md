## Curring

_Curring_ is not a monad: it is the technique of converting a function that takes multiple arguments into a sequence of functions that each take a single argument.  It was introduced by Gottlob Frege developed by Moses Schönfinkel, and further developed by *Haskell Curry*.

Mixing Higher order functions ( functions that return a function ) with moand is a very common programming style other functional programming languages. This is way it is included in this module.
With _curry_ decorator you can transform a function in a _curried_ function: just apss some positional parameters and get back a function with the remaining ones.

```python
@curry
def power(exp: int, base: int ) -> int:
    return math.pow(base, exp)

square_fn = power(2) # a function that returns the square of the parameter

```