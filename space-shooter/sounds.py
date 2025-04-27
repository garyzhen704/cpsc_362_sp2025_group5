import pygame

# Initialize mixer for sound
pygame.mixer.init()

# Load sound effects and music
pygame.mixer.music.load('space-shooter/sounds/background_sd.mp3')
pygame.mixer.music.set_volume(0.2)

shooting_sound = pygame.mixer.Sound('space-shooter/sounds/bullet_shot.mp3')
shooting_sound.set_volume(0.06)

death_sound = pygame.mixer.Sound('space-shooter/sounds/player_death.mp3')
death_sound.set_volume(0.6)

asteroid_exp_sounds = [
    pygame.mixer.Sound('space-shooter/sounds/asteroid_explode1.mp3'),
    pygame.mixer.Sound('space-shooter/sounds/asteroid_explode2.mp3'),
    pygame.mixer.Sound('space-shooter/sounds/asteroid_explode3.mp3'),
]
for sound in asteroid_exp_sounds:
    sound.set_volume(0.5)

powerup_sound = pygame.mixer.Sound('space-shooter/sounds/powerup.mp3')
powerup_sound.set_volume(0.25)

power_life_sound = pygame.mixer.Sound('space-shooter/sounds/extra_life.mp3')
power_life_sound.set_volume(0.3)

power_bullets_sound = pygame.mixer.Sound('space-shooter/sounds/faster_bullets.mp3')
power_bullets_sound.set_volume(0.3)

power_shield_sound = pygame.mixer.Sound('space-shooter/sounds/shield.mp3')
power_shield_sound.set_volume(0.3)

power_shrink_sound = pygame.mixer.Sound('space-shooter/sounds/shrink.mp3')
power_shrink_sound.set_volume(0.3)

# Play the background music in a loop
pygame.mixer.music.play(loops=-1, start=0.0)  # Loops indefinitely
