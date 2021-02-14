Represents a ordered sequence of items.

- Also implements `Monoid`.

```python

m_list: List[int] = List([1, 2, 4, 9])
for i in m_list:
    ...

#Or filter with a generator

evens: List[int] = [k for k in m_list if k % 2 == 0 ]

# And use it like a monad

doubles: List[int] = m_list.map(lambda i : i * 2) 

# Mixing and matching oop and fn

m_list.fold(lambda k, h: k + h, 0) == 16

```

#### Flatten

If you have a list of lists, and want to create one list (sequence) from them, use the flatten method to convert a list of lists into a single list

```python

m_list: List[Union[int, List[int]]] = List([1, 2, List([3, 4])])
len(m_list.flatten()) == 4

```