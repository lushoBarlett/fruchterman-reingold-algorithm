from math import sqrt
from random import random


class Vector2D:
    def zero():
        return Vector2D(0, 0)

    def random():
        return Vector2D(random(), random())

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __pos__(self):
        return Vector2D(self.x, self.y)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def distance(self, other):
        return abs(self - other)

    def normalized(self):
        return self / abs(self)
