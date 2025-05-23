from vector import Vector
import pygame

# Game window
screen_width = 1280
screen_height = 720
score = 0
high_score = 0
best_survival_time = "00:00:000"

game_over = False

# Frame rate
FPS = 30

# Colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

# Player spawn
player_start_pos = Vector(screen_width / 2, screen_height / 2)  # Start at screen center

# All game objects currently processing
game_objects = set()
player_bullets = []
asteroids = set()

def spawn_obj(obj):
    game_objects.add(obj)

def delete_obj(obj):
    if obj in game_objects:
        game_objects.remove(obj)
    if obj in player_bullets:
        player_bullets.remove(obj)
    if obj in asteroids:
        asteroids.remove(obj)

player = None