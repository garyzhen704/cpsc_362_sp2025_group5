import sys
import pygame
from pygame.locals import *
import globals as gl
from object import Object
from vector import Vector
from player import Player
from asteroid import Asteroid
import random
import time

# Font setup
pygame.init()
button_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 36) 

def reset_game():
    gl.game_objects.clear()
    gl.score = 0

    # Recreate player
    player = Player(gl.player_start_pos, gl.player_color)
    gl.player = player
    gl.spawn_obj(player)

    # Spawn asteroids again
    spawn_asteroids(5)
    return player

def draw_game_over(surface):
    # Dark overlay
    overlay = pygame.Surface((gl.screen_width, gl.screen_height))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))

    # "You Lose" text
    lose_text = button_font.render("You Lose!", True, (255, 50, 50))
    text_rect = lose_text.get_rect(center=(gl.screen_width // 2, gl.screen_height // 2 - 50))
    surface.blit(lose_text, text_rect)

    # "Play Again" button
    button_text = button_font.render("Play Again", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(gl.screen_width // 2, gl.screen_height // 2 + 30))
    pygame.draw.rect(surface, (100, 100, 255), button_rect.inflate(20, 10))
    surface.blit(button_text, button_rect)

    return button_rect

def spawn_asteroids(count=5):
    for _ in range(count):
        # Randomly choose a side to spawn the asteroid (top, bottom, left, or right)
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        # Based on the side, determine the position and velocity
        if side == 'top':
            pos = Vector(random.randint(0, gl.screen_width), 0)  # Spawn at the top
            velocity = Vector(random.uniform(-200, 200), random.uniform(100, 300))  # Moving down
        elif side == 'bottom':
            pos = Vector(random.randint(0, gl.screen_width), gl.screen_height)  # Spawn at the bottom
            velocity = Vector(random.uniform(-200, 200), random.uniform(-300, -100))  # Moving up
        elif side == 'left':
            pos = Vector(0, random.randint(0, gl.screen_height))  # Spawn on the left
            velocity = Vector(random.uniform(100, 300), random.uniform(-200, 200))  # Moving right
        elif side == 'right':
            pos = Vector(gl.screen_width, random.randint(0, gl.screen_height))  # Spawn on the right
            velocity = Vector(random.uniform(-300, -100), random.uniform(-200, 200))  # Moving left
        
        # Check if the spawn position is too close to the player and adjust it if needed
        if pos.distance_to(gl.player.position) < 50:  # Adjust this threshold if needed
            # Shift the asteroid's spawn position slightly if too close to the player
            pos += Vector(random.randint(50, 100), random.randint(50, 100))
        
        # Randomly generate the asteroid size
        size = random.randint(20, 30)
        
        # Create the asteroid and add it to the game
        asteroid = Asteroid(size, pos, velocity)
        gl.spawn_obj(asteroid)

def wrap(num, min, max):
    range_size = max - min + 1
    return (num - min) % range_size + min

def clamp_to_screen(obj: Object):
    if isinstance(obj.hitbox, pygame.Rect):
        x = wrap(obj.position.x, 0, gl.screen_width)
        y = wrap(obj.position.y, 0, gl.screen_height)
    else:
        radius = obj.hitbox.radius
        x = wrap(obj.position.x, -radius, gl.screen_width + radius)
        y = wrap(obj.position.y, -radius, gl.screen_height + radius)
    
    obj.position = Vector(x, y)

# Initialize pygame display
info = pygame.display.Info()
WINDOWED_SIZE = (gl.screen_width, gl.screen_height)
is_fullscreen = False
screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Space Shooter")
fps_clock = pygame.time.Clock()

# Load background
background = pygame.image.load("space-shooter/space_bg.jpg").convert()
background = pygame.transform.scale(background, (gl.screen_width, gl.screen_height))

# Create player and asteroids
player = Player(gl.player_start_pos, gl.WHITE)
gl.player = player
gl.spawn_obj(player)

# Add this at the start of your main loop, outside the loop
last_spawn_time = time.time()  # Record the start time 
delay_start_time = None  # Variable to track when the game actually starts

# Game loop
while True:
    gl.screen_width, gl.screen_height = screen.get_width(), screen.get_height()
    gl.player_start_pos = Vector(gl.screen_width / 2, gl.screen_height / 2)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if gl.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                button_rect = draw_game_over(screen)
                if button_rect.collidepoint(mouse_pos):
                    # Reset game
                    gl.game_over = False
                    gl.score = 0
                    gl.game_objects.clear()
                    player = Player(gl.player_start_pos, gl.player_color)
                    gl.spawn_obj(player)
                    spawn_asteroids(5)
                    continue

        if event.type == KEYDOWN:
            if event.key == pygame.K_f:
                is_fullscreen = not is_fullscreen
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if is_fullscreen else pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE)

            elif event.key == pygame.K_m:
                pygame.display.iconify()

            elif event.key == pygame.K_z:
                for obj in list(gl.game_objects):
                    if isinstance(obj, Asteroid):
                        obj.destroy()

    # Scale and draw background
    screen_width = gl.screen_width
    screen_height = gl.screen_height
    background_scaled = pygame.transform.scale(background, (screen_width, screen_height))
    screen.fill(gl.BLACK)
    screen.blit(background_scaled, (0, 0))

    if not gl.game_over:
        current_time = time.time()

        # Initialize delay_start_time when the player first starts the game
        if delay_start_time is None:
            delay_start_time = current_time

        # Wait for 3 seconds before spawning asteroids
        if current_time - delay_start_time >= 3:  # Wait for 3 seconds after game starts
            spawn_interval = 1  # Spawn a new asteroid every 5 seconds
            
            if current_time - last_spawn_time >= spawn_interval:
                spawn_asteroids(1)  # Spawn a new asteroid
                last_spawn_time = current_time  # Update the last spawn time

        # Update/draw game objects
        for obj in list(gl.game_objects):
            obj.update(gl.FPS)
            clamp_to_screen(obj)
            obj.draw(screen)
    else:
        button_rect = draw_game_over(screen)

    # Draw score
    score_text = font.render(f"Score: {gl.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {gl.high_score}", True, (255, 255, 0))
    screen.blit(high_score_text, (10, 40))  # Slightly below the score
    lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
    text_rect = lives_text.get_rect(topright=(gl.screen_width - 10, 10))
    screen.blit(lives_text, text_rect)

    pygame.display.update()
    fps_clock.tick(gl.FPS)
