

In abstract algebra, a monoid is a set equipped with an associative binary operation and an identity element. Monoids are semigroups with identity. Such algebraic structures occur in several branches of mathematics. For example, the functions from a set into itself form a monoid with respect to function composition. Many abstract data types can be endowed with a monoid structure. In a common pattern, a sequence of elements of a monoid is "folded" or "accumulated" to produce a final value.

#### mappend (`+`)

Describes an associative binary operation for a type.

#### mzero

Provides an identity value for the `mappend` operation.

#### mconcat

Accumulates a list of values using `mappend`. Returns the `mzero`
value if the list is empty.