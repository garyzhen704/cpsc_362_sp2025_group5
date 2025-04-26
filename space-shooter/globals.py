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
FPS = 60

#Initialize mixer for sound
pygame.mixer.init()
# Load sound effects and music
shooting_sound = pygame.mixer.Sound('space-shooter/sounds/bullet_shot.mp3')  # Path to sound file
explosion_sound = pygame.mixer.Sound('space-shooter/sounds/Explosion.mp3')
pygame.mixer.music.load('space-shooter/sounds/background_sd.wav')
# Set default volume for all sounds
shooting_sound.set_volume(0.06)  # Set shooting sound to 6% volume
explosion_sound.set_volume(0.5)  # Set explosion sound to 50% volume
# Set background music volume
pygame.mixer.music.set_volume(0.2)  # Set background music to 20% volume
# Play the background music in a loop
pygame.mixer.music.play(loops=-1, start=0.0)  # Loops indefinitely
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
player_bullets = []

def spawn_obj(obj):
    game_objects.add(obj)

def delete_obj(obj):
    if obj in game_objects:
        game_objects.remove(obj)
    if obj in player_bullets:
        player_bullets.remove(obj)

player = None