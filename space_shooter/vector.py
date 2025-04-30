import math

class Vector():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # Returns length of vector
    def magnitude(self) -> float:
        return (self.x * self.x + self.y * self.y) ** 0.5

    # Returns a copy of this vector with a length of 1
    def normalized(self):
        return self / self.magnitude()

    # Returns a copy of this vector moved towards another by a specified number of units
    def moved_toward(self, to: 'Vector', amount: float):
        dir = to - self
        if amount >= dir.magnitude():
            return to
        return self + (dir.normalized() * amount)

    # Returns a copy of this vector rotated by an angle in degrees
    def rotated(self, angle: float):
        rad = math.radians(angle)
        sin = math.sin(rad)
        cos = math.cos(rad)
        x1 = self.x * cos - self.y * sin
        y1 = self.x * sin + self.y * cos
        return Vector(x1, y1)

    def __add__(self, other: 'Vector'):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector'):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if scalar == 0:
            return Vector(0, 0)
        return Vector(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar):
        if scalar == 0:
            return Vector(0, 0)
        return Vector(self.x // scalar, self.y // scalar)

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def distance_to(self, other: 'Vector') -> float:
        """Calculate the Euclidean distance to another Vector."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
