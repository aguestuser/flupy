"""
Simple vector class

Supports addition:

>>> v1 = Vector(2, 4)
>>> v2 = Vector(2, 1)
>>> v1 + v2
Vector(4, 5)

Support absolute values:

>>> v = Vector(3, 4)
>>> abs(v)
5.0

Supports scalar multiplication:

>>> v * 3
Vector(9, 12)
>>> abs(v * 3)
15.0
"""

# TODO: write pytest tests!

from math import hypot


class Vector():

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __abs__(self) -> float:
        return hypot(self.x, self.y)

    def __bool__(self) -> bool:
        return bool(self.x or self.y)

    def __add__(self, other: 'Vector') -> 'Vector':
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar: int) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)
