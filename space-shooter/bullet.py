import pygame
from vector import Vector
import globals
from object import Object

# Bullet constants
BULLET_SPEED = 700  # Speed of the bullet (pixels per second)
BULLET_LIFETIME = .45  # Lifetime of the bullet (seconds)
BULLET_RADIUS = 6


class Bullet(Object):
    def __init__(self, pos: Vector, direction: Vector, player_vel: Vector, color):
        init_vel = (direction.normalized() * BULLET_SPEED) + player_vel
        super().__init__(BULLET_RADIUS, pos, init_vel, color)

        self.lifetime = BULLET_LIFETIME  # Seconds
        self.age = 0

    def update(self, fps: float):
        self.apply_velocity(fps)

        # Check for collisions with asteroids
        obj: Object
        for obj in globals.game_objects:
            from asteroid import Asteroid  # Lazy import to avoid circular import
            if isinstance(obj, Asteroid) and self.hitbox.is_colliding(obj):
                obj.destroy()  # Split or delete asteroid
                globals.delete_obj(self)
                return  # Bullet is gone, skip the rest

        self.age += 1 / fps
        # Destroy bullet if its lifetime exceeds limit
        if self.age > self.lifetime:
            globals.delete_obj(self)
