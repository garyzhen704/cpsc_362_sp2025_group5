from abc import ABC
import pygame
from globals import game_objects
from vector import Vector

# Abstract class
# Base class for all physical game objects
class Object(ABC):
    def __init__(self, hitbox_size: float, pos: Vector, vel: Vector, color):
        self.hitbox = Hitbox(self, hitbox_size)
        self.position = pos
        self.velocity = vel
        self.color = color
        print(f"{self} created")

    def __del__(self):
        print(f"{self} deleted")

    def delete(self):
        if self in game_objects:
            game_objects.remove(self)

    def update(self):
        self.apply_velocity()

    def apply_velocity(self):
        self.position += self.velocity

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, tuple(self.position), self.hitbox.size)


# All Objects contain a Hitbox which is used to detect "collisions"
class Hitbox():
    def __init__(self, owner: Object, size: float):
        self.owner = owner
        self.size = size

    def get_collisions(self):
        collisions = set()

        obj: Object
        for obj in game_objects:
            if obj == self.owner:
                continue

            other_size = obj.hitbox.size
            diff = abs(other_size - self.size)
            sum = other_size + self.size
            dist = (obj.position - self.owner.position).magnitude()

            # detect if 2 hitboxes are intersecting
            if diff <= dist and dist <= sum:
                collisions.add(obj)

        return collisions