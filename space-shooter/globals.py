from vector import Vector

# Game window
screen_width = 800
screen_height = 600

# Frame rate
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
player_color = WHITE
asteroid_color = GRAY

# Player spawn
player_start_pos = Vector(screen_width / 2, screen_height / 2)  # Start at screen center

# All game objects currently processing
game_objects = set()

def spawn_obj(obj):
    game_objects.add(obj)

def delete_obj(obj):
    if obj in game_objects:
        game_objects.remove(obj)
