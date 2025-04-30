import pygame
import os
import math
from object import Object
from vector import Vector
from bullet import Bullet  # Import the Bullet class
import globals
import sound
from asteroid import Asteroid

BASE_MAX_SPEED = 1080#360  # Pixels per second
BASE_ACCEL = 45 #15  # Pixels per second squared
BASE_DECEL = 1.5#0.5

SHRUNK_MAX_SPEED = 1440#480
SHRUNK_ACCEL = 180 #60
SHRUNK_DECEL = 60 #20

BASE_RADIUS = 8  # Radius of player hitbox
SHRUNK_RADIUS = 4  # While shrink powerup is active

BASE_FIRE_RATE = 0.065 #0.2  # In seconds
MAX_BULLETS = 20

DMG_COOLDOWN = 4  # How many seconds the player is invulnerable after taking damage
TRANSPARENCY = 0.7  # How much transparency to add when in damage cooldown
MAX_RED_TINT = 70  # 0-255, how much red to apply when at 1 life

def lerp_angle(a, b, t):
    """Linearly interpolate between two angles in degrees."""
    diff = (b - a + 180) % 360 - 180
    return a + diff * t


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


class Player(Object):
    def __init__(self, pos: Vector):
        hitbox_radius = BASE_RADIUS

        super().__init__(hitbox_radius, pos, Vector(0, 0), globals.WHITE)

        self.frames = self.load_frames("frames")
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        self.angle = 0  # Current visual angle
        self.target_angle = 0  # Where the ship wants to point

        self.shoot_timer = 0  # How much time has passed since the last shot
        self.fire_rate = BASE_FIRE_RATE

        self.hit_timer = DMG_COOLDOWN  # How much time has passed since taking damage
        self.game_over = False  # Flag to indicate the game is over
        self.lives = 3

        self.shield_image = pygame.image.load("powerups/spr_shield.png").convert_alpha()
        self.shield_timer = 0  # Add if not already present

        self.ship_scale = 1.0
        self.shrink_timer = 0


    def register_hit(self):
        if self.shield_timer > 0:
            return
            
        self.hit_timer = 0
        self.lives -= 1

        if self.lives == 1:
            sound.last_life_sound.play(3)

        if self.lives == 0:
            sound.death_sound.play()
            globals.game_over = True
            if globals.score > globals.high_score:
                globals.high_score = globals.score
        else:
            sound.hurt_sound.play()


    def load_frames(self, folder_path):
        frame_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])
        return [pygame.image.load(os.path.join(folder_path, f)).convert_alpha() for f in frame_files]


    def update(self, fps: float):
        input_dir = get_input_dir()
        throttle_on = input_dir.magnitude() > 0.1

        speed, acceleration, deceleration = BASE_MAX_SPEED, BASE_ACCEL, BASE_DECEL
        if self.shrink_timer > 0:
            speed = SHRUNK_MAX_SPEED
            acceleration = SHRUNK_ACCEL
            deceleration = SHRUNK_DECEL

        # Apply movement
        target_vel = input_dir * speed
        self.velocity = self.velocity.moved_toward(target_vel, acceleration if throttle_on else deceleration)
        self.apply_velocity(fps)

        # Detect collisions with asteroids
        self.hit_timer += 1 / fps
        if self.hit_timer > DMG_COOLDOWN:
            for obj in globals.game_objects.copy():
                if isinstance(obj, Asteroid):
                    if self.hitbox.is_colliding(obj):
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

        if self.shoot_timer < self.fire_rate:
            self.shoot_timer += 1 / fps
        # Shoot when spacebar is pressed and timer has reached target time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.shoot_timer > self.fire_rate:
            print('spacebar pressed')
            self.shoot()
            self.shoot_timer -= self.fire_rate

        # Decrement timers to 0
        self.shield_timer = max(self.shield_timer - (1 / fps), 0)
        self.shrink_timer = max(self.shrink_timer - (1 / fps), 0)

        if self.shrink_timer > 0:
            self.hitbox.radius = SHRUNK_RADIUS
        else:
            self.hitbox.radius = BASE_RADIUS
        self.ship_scale = self.hitbox.radius / BASE_RADIUS


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
        sound.shooting_sound.play()
        print('bullet created')


    def draw(self, surface):
        frame = self.frames[self.current_frame]

        # Scale the sprite based on ship_scale (for shrink power-up)
        scaled_size = (
            int(frame.get_width() * self.ship_scale),
            int(frame.get_height() * self.ship_scale)
        )
        frame = pygame.transform.scale(frame, scaled_size)

        # Rotate the spaceship based on smoothed angle
        rotated_frame = pygame.transform.rotate(frame, self.angle)

        # Add transparency while in damage cooldown
        if self.hit_timer < DMG_COOLDOWN:
            rotated_frame.set_alpha(int(255 * TRANSPARENCY))

        # Apply red tint at 1 life
        if self.lives == 1:
            red_tint = pygame.Surface(rotated_frame.get_size(), flags=pygame.SRCALPHA)
            red_tint.fill((MAX_RED_TINT, 0, 0, 0))
            rotated_frame.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Center the rotated image
        rect = rotated_frame.get_rect(center=(self.position.x, self.position.y))
        surface.blit(rotated_frame, rect)

        if self.shield_timer > 0:
            # Scale the shield based on ship_scale too
            shield_size = int(70 * self.ship_scale)
            shield_scaled = pygame.transform.scale(self.shield_image, (shield_size, shield_size))
            shield_rect = shield_scaled.get_rect(center=(self.position.x, self.position.y))
            surface.blit(shield_scaled, shield_rect)
