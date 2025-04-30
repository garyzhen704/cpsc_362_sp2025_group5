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
import powerup
from powerup import PowerUp
import asyncio




async def main():
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
        
        spawns_left = max(max_asteroids - len(gl.asteroids), 0)
        final_count = min(count, spawns_left)

        if final_count != count:
            print(f"max asteroids reached ({len(gl.asteroids)}/{max_asteroids})")
            print(f"spawned {final_count} asteroids instead of {count}")

        for _ in range(final_count):
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
            size = random.randint(1, 5)

            # Create the asteroid and add it to the game
            asteroid = Asteroid(size, pos, velocity)
            gl.spawn_obj(asteroid)


    def spawn_powerup():
        # Randomly choose a type of power-up
        types = PowerUp.TYPES.copy()
        # Do not choose fast_bullets if already at max upgrade
        if gl.player.fire_rate <= powerup.MIN_FIRE_RATE:
            types.remove("fast_bullets")

        powerup_type = random.choice(types)

        # Randomly spawn position on the screen
        spawn_x = random.randint(0, gl.screen_width)
        spawn_y = random.randint(0, gl.screen_height)
        pos = Vector(spawn_x, spawn_y)

        new_powerup = PowerUp(pos, powerup_type)
        gl.spawn_obj(new_powerup)


    def wrap(num, min, max):
        range_size = max - min + 1
        return (num - min) % range_size + min


    def clamp_to_screen(obj: Object):
        radius = obj.hitbox.radius
        x = wrap(obj.position.x, -radius, gl.screen_width + radius)
        y = wrap(obj.position.y, -radius, gl.screen_height + radius)

        obj.position = Vector(x, y)


    def get_survival_time():
        
        if game_start_time:  # Only calculate if the start time is set
            elapsed_time_ms = pygame.time.get_ticks() - game_start_time  # Time in milliseconds
            minutes = elapsed_time_ms // 60000  # Convert to minutes
            seconds = (elapsed_time_ms % 60000) // 1000  # Convert to seconds
            milliseconds = (elapsed_time_ms % 1000)  # Remaining milliseconds

            # Return formatted time string
            return f"{minutes:02}:{seconds:02}:{milliseconds:03}"
        return "00:00:000"  # Default return when no start time is set


    def get_dynamic_spawn_interval():
        
        
        """Calculate the dynamic spawn interval based on the time survived."""
        if game_start_time is None:
            return SPAWN_INTERVAL_START

        elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000  # Elapsed time in seconds

        # Decrease spawn rate (interval) over time until it hits the minimum value
        new_interval = max(SPAWN_INTERVAL_MIN, SPAWN_INTERVAL_START - (elapsed_time * SPAWN_INTERVAL_DECAY))

        return new_interval
    # Font setup
    pygame.init()
    button_font = pygame.font.Font(None, 48)
    font = pygame.font.Font(None, 24)

    # Initialize pygame display
    info = pygame.display.Info()
    WINDOWED_SIZE = (gl.screen_width, gl.screen_height)
    is_fullscreen = False
    screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Space Shooter")
    fps_clock = pygame.time.Clock()

    # Load background
    background = pygame.image.load("images/space_bg.jpg").convert()
    background = pygame.transform.scale(background, (gl.screen_width, gl.screen_height))

    # Create player and asteroids
    gl.player = Player(gl.player_start_pos)
    gl.spawn_obj(gl.player)

    # Constants for spawn rate control
    SPAWN_INTERVAL_START = 7  # Start at 8 seconds
    SPAWN_INTERVAL_MIN = 1.5   # Minimum spawn interval (cap)
    SPAWN_INTERVAL_DECAY = .05  # Rate at which spawn interval decreases

    max_asteroids = 20
    spawn_interval = 2  # Spawn a new asteroid every 2 seconds
    last_spawn_time = time.time()  # Track when the last asteroid was spawned

    last_powerup_time = time.time()  # Track when the last power-up was spawned
    powerup_spawn_interval = 10  # Power-ups spawn every 10 seconds

    game_start_time = None
    final_survival_time = None

    show_debug_hitboxes = False

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
                        for obj in gl.game_objects.copy():
                            gl.delete_obj(obj)

                        game_start_time = pygame.time.get_ticks()  # Set the start time again if it's None
                        final_survival_time = None #Resetting final time that shows up in end screen

                        gl.player = Player(gl.player_start_pos)
                        gl.spawn_obj(gl.player)

                        continue

            if event.type == KEYDOWN:
                if event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if is_fullscreen else pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE)

                elif event.key == pygame.K_m:
                    pygame.display.iconify()

                # elif event.key == pygame.K_z:
                #     for obj in list(gl.game_objects):
                #         if isinstance(obj, Asteroid):
                #             obj.destroy()

        # Scale and draw background
        screen_width = gl.screen_width
        screen_height = gl.screen_height
        background_scaled = pygame.transform.scale(background, (screen_width, screen_height))
        screen.fill(gl.BLACK)
        screen.blit(background_scaled, (0, 0))

        if not gl.game_over:
            current_time = time.time()
            if game_start_time is None:
                game_start_time = pygame.time.get_ticks()  # Start survival timer
            
            spawn_interval = get_dynamic_spawn_interval()  # Update spawn interval based on time

            if current_time - last_spawn_time >= spawn_interval:
                spawn_asteroids(1)  # Spawn a new asteroid
                last_spawn_time = current_time  # Update last spawn time

            # Power-up spawning logic
            if current_time - last_powerup_time >= powerup_spawn_interval:
                spawn_powerup()
                last_powerup_time = current_time  # Update the last power-up spawn time

            # Update/draw game objects
            for obj in list(gl.game_objects):
                obj.update(gl.FPS)
                clamp_to_screen(obj)
                obj.draw(screen)
                if show_debug_hitboxes:
                    obj.debug_draw(screen)

            # Check if the game has just ended
            if gl.game_over and final_survival_time is None:
                final_survival_time = get_survival_time()

                # Compare to best time and update if it's better
                current_time_ms = pygame.time.get_ticks() - game_start_time
                best_time_parts = [int(p) for p in gl.best_survival_time.replace(":", "").split()]
                best_time_ms = int(gl.best_survival_time[0:2]) * 60000 + int(gl.best_survival_time[3:5]) * 1000 + int(gl.best_survival_time[6:9])

                if current_time_ms > best_time_ms:
                    gl.best_survival_time = final_survival_time

        else:
            button_rect = draw_game_over(screen)
            if final_survival_time:
                # Show final survival time
                time_text = font.render(f"Survived: {final_survival_time} seconds", True, (200, 200, 255))
                time_rect = time_text.get_rect(center=(gl.screen_width // 2, gl.screen_height // 2 + 80))
                screen.blit(time_text, time_rect)

        # Draw score
        score_text = font.render(f"Score: {gl.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        high_score_text = font.render(f"High Score: {gl.high_score}", True, (255, 255, 0))
        screen.blit(high_score_text, (10, 40))  # Slightly below the score
        lives_text = font.render(f"Lives: {gl.player.lives}", True, (255, 255, 255))
        text_rect = lives_text.get_rect(topright=(gl.screen_width - 10, 10))
        screen.blit(lives_text, text_rect)
        survival_best_text = font.render(f"Best Time: {gl.best_survival_time}", True, (0, 255, 255))
        survival_best_rect = survival_best_text.get_rect(topright=(gl.screen_width - 10, text_rect.bottom + 5))
        screen.blit(survival_best_text, survival_best_rect)

        # Show survival time while playing
        if not gl.game_over:
            survival_time = get_survival_time()
            time_text = font.render(f"Time: {survival_time}s", True, (200, 200, 255))
            screen.blit(time_text, (10, 70))

        pygame.display.update()
        fps_clock.tick(gl.FPS)
        await asyncio.sleep(0)
asyncio.run(main())
