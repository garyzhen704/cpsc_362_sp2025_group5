import pygame
import random
import globals
from object import Object
from vector import Vector
import player

# Constants
min_speed = 300.0
max_speed = 600.0
piece_max_angle_offset = 75.0
piece_speed_offset = 80.0
size_to_pixel_ratio = 10


class Asteroid(Object):
    asteroid_img = None  # Define the class variable to store the image

    @classmethod
    def load_image(cls):
        if cls.asteroid_img is None:
            cls.asteroid_img = pygame.image.load("space-shooter/asteroid.png").convert_alpha()

    def __init__(self, size: float, pos: Vector, vel: Vector):
        self.__class__.load_image()  # Make sure the image is loaded

        self.size = size
        self.angle = 0
        self.rotation = random.uniform(-60, 60)  # degrees per second

        # Cap velocity
        new_vel = vel
        if new_vel.magnitude() < min_speed:
            new_vel = new_vel.normalized() * min_speed
        elif new_vel.magnitude() > max_speed:
            new_vel = new_vel.normalized() * max_speed
        
        visual_diameter = size * size_to_pixel_ratio  # this is used for image scaling
        hitbox_radius = int(visual_diameter * 0.4)  # tune 0.4 as needed    

        super().__init__(hitbox_radius, pos, new_vel, None)

        self.original_image = pygame.transform.scale(self.__class__.asteroid_img, (visual_diameter, visual_diameter))

        # Prepare scaled image
        scaled_size = int(size * size_to_pixel_ratio)
        self.original_image = pygame.transform.scale(self.__class__.asteroid_img, (scaled_size, scaled_size))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

    def update(self, fps: float):
        # Apply movement
        self.position += self.velocity * (1 / fps)

        # Rotate asteroid
        self.angle += self.rotation * (1 / fps)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        for obj in globals.game_objects:
            if isinstance(obj, player.Player):
                # Use circular collision (distance between centers < sum of radii)
                distance = self.position.distance_to(obj.position)
                if distance < self.hitbox.radius + obj.hitbox.radius:
                    obj.register_hit()
                    self.destroy()
                    break

    def draw(self, surface):
        self.rect.center = (self.position.x, self.position.y)
        surface.blit(self.image, self.rect)

    def destroy(self):
        MIN_SIZE = 5  # Minimum size for asteroid pieces
        if self.size > MIN_SIZE:
            angle1 = random.random() * 360.0
            angle2 = angle1 + 180.0 + random.uniform(-piece_max_angle_offset, piece_max_angle_offset)

            # Calculate the size for the pieces, ensuring it doesn't go below MIN_SIZE
            half_size = max(self.size // 2, MIN_SIZE)  # Ensure the piece is not too small
            remaining_size = max(self.size - half_size, MIN_SIZE)  # Ensure the second piece is not too small

            self._spawn_piece(half_size, angle1)
            self._spawn_piece(remaining_size, angle2)
        globals.score += 10
        globals.delete_obj(self)

    def _spawn_piece(self, size, angle):
        vel_add = self.velocity.normalized() * random.uniform(-piece_speed_offset, piece_speed_offset)
        new_velocity = (self.velocity + vel_add).rotated(angle)
        globals.spawn_obj(Asteroid(size, self.position, new_velocity))
