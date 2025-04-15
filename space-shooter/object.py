from abc import ABC
import pygame
from globals import game_objects
from vector import Vector

# Abstract class
# Base class for all physical game objects
class Object(ABC):
    def __init__(self, hitbox_radius: float, pos: Vector, vel: Vector, color):
        self.hitbox = Hitbox(self, hitbox_radius)
        self.position = pos
        self.velocity = vel
        self.color = color
        print(f"{self} created")

    def __del__(self):
        print(f"{self} deleted")

    def update(self, fps: float):
        self.apply_velocity(fps)

    def apply_velocity(self, fps: float):
        self.position += self.velocity / fps

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, tuple(self.position), self.hitbox.radius)


# All Objects contain a Hitbox which is used to detect "collisions"
class Hitbox():
    def __init__(self, owner: Object, radius: float):
        self.owner = owner
        self.radius = radius

    def get_collisions(self):
        collisions = set()

        obj: Object
        for obj in game_objects:
            if obj == self.owner:
                continue

            other_radius = obj.hitbox.radius
            diff = abs(other_radius - self.radius)
            sum = other_radius + self.radius
            dist = (obj.position - self.owner.position).magnitude()

            # detect if 2 hitboxes are intersecting
            if diff <= dist and dist <= sum:
                collisions.add(obj)

        return collisions