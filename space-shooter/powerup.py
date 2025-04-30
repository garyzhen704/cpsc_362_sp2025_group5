# powerup.py
import pygame
from object import Object
from vector import Vector
import globals
import sound

POWERUP_VIS_RADIUS = 15
POWERUP_HITBOX_RADIUS = 25
POWERUP_DURATION = 8  # seconds for temporary effects
MIN_FIRE_RATE = 0.07  # Lowest fire rate possible

class PowerUp(Object):
    TYPES = ['life', 'fast_bullets', 'shield', 'shrink']
    COLORS = {
        'life': (0, 255, 0),
        'fast_bullets': (255, 165, 0),
        'shield': (0, 200, 255),
        'shrink': (200, 0, 255),
    }

    def __init__(self, pos: Vector, powerup_type: str):
        super().__init__(POWERUP_HITBOX_RADIUS, pos, Vector(0, 0), self.COLORS[powerup_type])
        self.type = powerup_type
        self.spawn_time = pygame.time.get_ticks()

        # Load the frames from the folder
        self.frames = self.load_frames(powerup_type)
        self.frame_index = 0  # To track the current frame
        self.animation_speed = 0.1  # How fast the frames change
        self.animation_timer = 0  # Timer to handle animation speed

    def load_frames(self, powerup_type: str):
        # Load the frames from the appropriate directory
        frames = []
        for i in range(1, 7):  # Assuming there are 6 frames per power-up type
            frame = pygame.image.load(f"powerups/Spnning Orb/{powerup_type}/frame {i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (POWERUP_VIS_RADIUS * 2, POWERUP_VIS_RADIUS * 2))
        
            frames.append(frame)
        return frames

    def update(self, fps: float):
        # Animate the sprite
        self.animation_timer += 1 / fps
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        current_time = pygame.time.get_ticks()
        if (current_time - self.spawn_time) / 1000 >= POWERUP_DURATION:  # Check if it exceeds the lifespan
            globals.delete_obj(self)  # Remove the power-up if it's expired
            return  # Stop further updates for this power-up

        # Check if the power-up is picked up
        if self.hitbox.is_colliding(globals.player):
            self.activate(globals.player)
            globals.delete_obj(self)

    def draw(self, surface):
        # Draw the current frame of the animation
        current_frame = self.frames[self.frame_index]
        rect = current_frame.get_rect(center=(self.position.x, self.position.y))
        surface.blit(current_frame, rect)

    def activate(self, player):
        sound.powerup_sound.play()

        if self.type == 'life':
            player.lives += 1
            sound.power_life_sound.play()

        elif self.type == 'fast_bullets':
            # Increase bullet speed permanently, with a cap
            player.fire_rate = max(player.fire_rate - 0.015, MIN_FIRE_RATE)
            sound.power_bullets_sound.play()

        elif self.type == 'shield':
            player.shield_timer = POWERUP_DURATION
            sound.power_shield_sound.play()

        elif self.type == 'shrink':
            player.shrink_timer = POWERUP_DURATION
            sound.power_shrink_sound.play()
