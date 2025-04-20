import pygame
from vector import Vector
import globals

# Bullet constants
BULLET_SPEED = 700  # Speed of the bullet (pixels per second)
BULLET_LIFETIME = .4  # Lifetime of the bullet (seconds)

class Bullet:
    def __init__(self, pos: Vector, direction: Vector, player_vel: Vector, color):
        self.position = pos
        self.velocity = (direction.normalized() * BULLET_SPEED) + player_vel
        self.color = color
        self.lifetime = BULLET_LIFETIME  # Seconds
        self.age = 0
        self.radius = 5  # Radius of the bullet (for collisions)
        
        # Rectangular hitbox for collision detection
        self.hitbox = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)
        
    def update(self, fps: float):
        # Move the bullet
        self.position += self.velocity * (1 / fps)
        self.age += 1 / fps

        # Update hitbox position
        self.hitbox.topleft = (self.position.x - self.radius, self.position.y - self.radius)

        # Check for collisions with asteroids
        for obj in list(globals.game_objects):
            from asteroid import Asteroid  # Lazy import to avoid circular import
            if isinstance(obj, Asteroid) and self.hitbox.colliderect(obj.rect):
                obj.destroy()  # Split or delete asteroid
                globals.delete_obj(self)
                return  # Bullet is gone, skip the rest

        # Destroy bullet if its lifetime exceeds limit
        if self.age > self.lifetime:
            globals.delete_obj(self)

    def draw(self, surface):
        # Draw the bullet as a circle (or rectangle if you want to change the shape)
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)
