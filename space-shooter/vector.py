class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self) -> float:
        return (self.x * self.x + self.y * self.y) ** 0.5
    
    def normalized(self) -> 'Vector':
        if (self.magnitude() > 1):
            pass
        return self / self.magnitude()

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
