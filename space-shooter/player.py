import pygame
import os
import math
from object import Object
from vector import Vector
from bullet import Bullet  # Import the Bullet class
import globals
from asteroid import Asteroid

max_speed = 360  # Pixels per second
acceleration = 15  # Pixels per second squared
deceleration = 0.5  # Deceleration rate
fire_rate = 0.07  # In seconds
dmg_cooldown = 4  # How many seconds the player is invulnerable after taking damage
transparency = 0.7  # How much transparency to add when in damage cooldown
MAX_BULLETS = 10

def lerp_angle(a, b, t):
    """Linearly interpolate between two angles in degrees."""
    diff = (b - a + 180) % 360 - 180
    return a + diff * t

class Player(Object):
    def __init__(self, pos: Vector, color):
        hitbox_radius = 8

        super().__init__(hitbox_radius, pos, Vector(0, 0), color)

        self.frames = self.load_frames("space-shooter/frames")
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        self.angle = 0  # Current visual angle
        self.target_angle = 0  # Where the ship wants to point

        self.shoot_timer = 0  # How much time has passed since the last shot
        self.hit_timer = dmg_cooldown  # How much time has passed since taking damage

        self.hits = 0  # Add a counter for hits
        self.max_hits = 2  # Maximum number of hits before the game ends
        self.game_over = False  # Flag to indicate the game is over
        self.lives = 2

    def register_hit(self):
        self.hit_timer = 0
        self.lives -= 1
        self.hits += 1
        if self.lives == 0:
            globals.game_over = True

    def load_frames(self, folder_path):
        frame_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])
        return [pygame.image.load(os.path.join(folder_path, f)).convert_alpha() for f in frame_files]

    def update(self, fps: float):
        input_dir = get_input_dir()
        throttle_on = input_dir.magnitude() > 0.1

        # Apply movement
        target_vel = input_dir * max_speed
        self.velocity = self.velocity.moved_toward(target_vel, acceleration if throttle_on else deceleration)
        self.apply_velocity(fps)

        self.hit_timer += 1 / fps
        if self.hit_timer > dmg_cooldown:
            for obj in globals.game_objects.copy():
                if isinstance(obj, Asteroid):
                    if self.hitbox.radius + obj.hitbox.radius > self.position.distance_to(obj.position):
                        self.register_hit()
                        obj.destroy()

        # Calculate desired rotation based on input direction
        if input_dir.magnitude() > 0:
            self.target_angle = math.degrees(math.atan2(-input_dir.y, input_dir.x)) - 90

        # Smoothly rotate toward target angle
        self.angle = lerp_angle(self.angle, self.target_angle, 0.15)

        # Animate spaceship
        self.animation_timer += 1 / fps
        if self.animation_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = 0

        self.shoot_timer += 1 / fps
        # Shoot when spacebar is pressed and timer has reached target time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.shoot_timer > fire_rate:
            print('spacebar pressed')
            self.shoot()
            self.shoot_timer = 0

    def shoot(self):
        if len(globals.player_bullets) >= MAX_BULLETS:
            oldest_bullet = globals.player_bullets[0]  # Delete the oldest bullet
            globals.delete_obj(oldest_bullet)

        # Correct angle so the bullet shoots from the front of the ship
        facing_angle = self.angle - 90
        radians = math.radians(facing_angle)
        direction = Vector(-math.cos(radians), math.sin(radians))

        offset = direction.normalized() * 20  # 20 pixels in front
        bullet = Bullet(self.position + offset, direction, self.velocity, pygame.Color('orange'))
        globals.player_bullets.append(bullet)
        globals.spawn_obj(bullet)
        print('bullet created')

    def draw(self, surface):
        frame = self.frames[self.current_frame]

        # Rotate the spaceship based on smoothed angle
        rotated_frame = pygame.transform.rotate(frame, self.angle)

        # Add transparency while in damage cooldown
        if self.hit_timer < dmg_cooldown:
            rotated_frame.set_alpha(int(255 * transparency))

        # Center the rotated image
        rect = rotated_frame.get_rect(center=(self.position.x, self.position.y))
        surface.blit(rotated_frame, rect)

def get_input_dir() -> Vector:
    dir = Vector(0, 0)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dir.x -= 1.0
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dir.x += 1.0
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dir.y -= 1.0
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dir.y += 1.0

    return dir.normalized()
