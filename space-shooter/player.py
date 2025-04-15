import pygame
from pygame.locals import *
from object import Object
from vector import Vector

def get_input_dir() -> Vector:
    dir = Vector(0, 0)

    keys = pygame.key.get_pressed()
    if keys[K_LEFT] or keys[K_a]:
        dir.x -= 1.0
    if keys[K_RIGHT] or keys[K_d]:
        dir.x += 1.0
    if keys[K_UP] or keys[K_w]:
        dir.y -= 1.0
    if keys[K_DOWN] or keys[K_s]:
        dir.y += 1.0

    return dir.normalized()


hitbox_radius = 15
max_speed = 360  # Pixels per sec
acceleration = 15  # Pixels per sec ^ 2
deceleration = 0.5


class Player(Object):
    def __init__(self, pos: Vector, color):
        super().__init__(hitbox_radius, pos, Vector(0, 0), color)

    def update(self, fps: float):
        input_dir = get_input_dir()
        throttle_on = input_dir.magnitude() > 0.1

        target_vel = input_dir * max_speed
        self.velocity = self.velocity.moved_toward(target_vel, (acceleration if throttle_on else deceleration))
        self.apply_velocity(fps)

        collisions = self.hitbox.get_collisions()
        if collisions:
            print(collisions)
