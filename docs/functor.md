## Functor

In mathematics, specifically category theory, a functor is a mapping between categories. In python is an object tha can be mapped to something else.

#### map (`*`)

Applies a function to the contents of a functor, transforming it from
one thing to another.

The `*` operator implements map on functors

```python
def wordcount(s: str):
    return len(s.split())


f.map(wordcount) ==  f * wordcount
```