class Vector():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # Returns length of vector
    def magnitude(self) -> float:
        return (self.x * self.x + self.y * self.y) ** 0.5

    # Returns a copy of this vector with a length of 1
    def normalized(self) -> 'Vector':
        return self / self.magnitude()

    # Returns a copy of this vector moved towards another by a specified number of units
    def moved_toward(self, to: 'Vector', amount: float) -> 'Vector':
        dir = to - self
        if amount >= dir.magnitude():
            return to
        return self + (dir.normalized() * amount)

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar) -> 'Vector':
        if scalar == 0:
            return Vector(0, 0)
        return Vector(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar) -> 'Vector':
        if scalar == 0:
            return Vector(0, 0)
        return Vector(self.x // scalar, self.y // scalar)

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
