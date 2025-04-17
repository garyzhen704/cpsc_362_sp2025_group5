from abc import ABC
import pygame
import globals
from globals import game_objects
from vector import Vector
import math

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
class Hitbox:
    def __init__(self, owner: Object, radius: float = None, rect: pygame.Rect = None):
        self.owner = owner
        if radius is not None:
            self.radius = radius  # For circular hitbox
            self.rect = None  # No rectangle hitbox
        elif rect is not None:
            self.rect = rect  # For rectangular hitbox
            self.radius = None  # No circular hitbox

    def get_collisions(self):
        collisions = []

        for obj in globals.game_objects:
            if obj == self.owner:  # Skip the object itself
                continue

            # Check if the other object has a rectangular hitbox
            if self.rect and isinstance(obj.hitbox.rect, pygame.Rect):  # Rectangular hitbox
                if self.rect.colliderect(obj.hitbox.rect):  # Check if rects collide
                    collisions.append(obj)

            # Check if the other object has a circular hitbox
            elif self.radius and hasattr(obj.hitbox, 'radius'):  # Circular hitbox
                # Calculate the distance between the centers of the two circles
                distance = self.owner.position.distance_to(obj.hitbox.owner.position)
                if distance < self.radius + obj.hitbox.radius:
                    collisions.append(obj)

        return collisions

