from abc import ABC
import pygame
import globals
from vector import Vector
import sys

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
        sys.__stdout__.write(f"{self} deleted\n")

    def update(self, fps: float):
        self.apply_velocity(fps)

    def apply_velocity(self, fps: float):
        self.position += self.velocity / fps

    def draw(self, screen: pygame.Surface):
        self.debug_draw(screen)
    
    def debug_draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, tuple(self.position), self.hitbox.radius)


# All Objects contain a Hitbox which is used to detect "collisions"
class Hitbox:
    def __init__(self, owner: Object, radius: float):
        self.owner = owner
        self.radius = radius

    def is_colliding(self, other: Object):
        # Calculate the distance between the centers of the two circles
        return self.owner.position.distance_to(other.position) < self.radius + other.hitbox.radius

    def get_collisions(self):
        collisions = set()

        obj: Object
        for obj in globals.game_objects:
            if obj == self.owner:  # Skip the object itself
                continue

            if self.is_colliding(obj):
                collisions.add(obj)

        return collisions
