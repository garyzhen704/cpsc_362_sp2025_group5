import pygame
import random
import globals
import sounds
from object import Object
from vector import Vector

# Constants
MIN_SPEED = 300.0
MAX_SPEED = 600.0
PIECE_MAX_ANG_OFFSET = 75.0
PIECE_SPD_OFFSET = 80.0
SIZE_PIXEL_RATIO = 50
MIN_SIZE = 1  # Minimum size for asteroid pieces


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
        if new_vel.magnitude() < MIN_SPEED:
            new_vel = new_vel.normalized() * MIN_SPEED
        elif new_vel.magnitude() > MAX_SPEED:
            new_vel = new_vel.normalized() * MAX_SPEED
        
        visual_diameter = size * SIZE_PIXEL_RATIO  # this is used for image scaling
        hitbox_radius = int(visual_diameter * 0.4)  # tune 0.4 as needed    

        super().__init__(hitbox_radius, pos, new_vel, globals.GRAY)

        self.original_image = pygame.transform.scale(self.__class__.asteroid_img, (visual_diameter, visual_diameter))

        # Prepare scaled image
        scaled_size = int(size * SIZE_PIXEL_RATIO)
        self.original_image = pygame.transform.scale(self.__class__.asteroid_img, (scaled_size, scaled_size))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

        globals.asteroids.add(self)

    def update(self, fps: float):
        # Apply movement
        self.position += self.velocity * (1 / fps)

        # Rotate asteroid
        self.angle += self.rotation * (1 / fps)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

    def draw(self, surface):
        self.rect.center = (self.position.x, self.position.y)
        surface.blit(self.image, self.rect)

    def destroy(self):
        if self.size > MIN_SIZE:
            angle1 = random.random() * 360.0
            angle2 = angle1 + 180.0 + random.uniform(-PIECE_MAX_ANG_OFFSET, PIECE_MAX_ANG_OFFSET)

            # Calculate the size for the pieces, ensuring it doesn't go below MIN_SIZE
            half_size = max(self.size // 2, MIN_SIZE)  # Ensure the piece is not too small
            remaining_size = max(self.size - half_size, MIN_SIZE)  # Ensure the second piece is not too small

            self._spawn_piece(half_size, angle1)
            self._spawn_piece(remaining_size, angle2)
        globals.score += 10
        globals.delete_obj(self)

        random.choice(sounds.asteroid_exp_sounds).play()

    def _spawn_piece(self, size, angle):
        vel_add = self.velocity.normalized() * random.uniform(-PIECE_SPD_OFFSET, PIECE_SPD_OFFSET)
        new_velocity = (self.velocity + vel_add).rotated(angle)
        globals.spawn_obj(Asteroid(size, self.position, new_velocity))
