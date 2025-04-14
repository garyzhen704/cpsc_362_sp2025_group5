import pygame
from pygame.locals import *
import sys
from vector import Vector

pygame.init()

# Set game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Set frame rate
FPS = 60
fps_clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player properties
player_size = 15
player_pos = Vector(screen_width / 2, screen_height / 2)  # Start at screen center
player_vel = Vector(0, 0)
player_max_speed = 360  # Pixels per sec
player_accel = 15  # Pixels per sec ^ 2
player_decel = 0.5


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


def clamped_to_screen(vec: Vector) -> Vector:
    return Vector(vec.x % screen_width, vec.y % screen_height)


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    input_dir = get_input_dir()
    throttle_on = input_dir.magnitude() > 0.1

    target_vel = input_dir * (player_max_speed / FPS)
    player_vel = player_vel.moved_toward(target_vel, (player_accel if throttle_on else player_decel) / FPS)
    
    player_pos += player_vel
    player_pos = clamped_to_screen(player_pos)

    # Draw shapes
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, tuple(player_pos), player_size)
    pygame.display.update()

    fps_clock.tick(FPS)
