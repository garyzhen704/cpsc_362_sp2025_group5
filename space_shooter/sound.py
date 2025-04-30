import pygame

# Initialize mixer for sound
pygame.mixer.init()

# Load sound effects and music
pygame.mixer.music.load('sounds/background_sd.wav')
pygame.mixer.music.set_volume(0.2)

shooting_sound = pygame.mixer.Sound('sounds/bullet_shot.wav')
shooting_sound.set_volume(0.06)

death_sound = pygame.mixer.Sound('sounds/player_death.wav')
death_sound.set_volume(0.6)

hurt_sound = pygame.mixer.Sound('sounds/player_dmg.wav')
hurt_sound.set_volume(0.4)

last_life_sound = pygame.mixer.Sound('sounds/last_life_alert.wav')
last_life_sound.set_volume(0.5)

asteroid_exp_sounds = [
    pygame.mixer.Sound('sounds/asteroid_explode1.wav'),
    pygame.mixer.Sound('sounds/asteroid_explode2.wav'),
    pygame.mixer.Sound('sounds/asteroid_explode3.wav'),
]
for sound in asteroid_exp_sounds:
    sound.set_volume(0.5)

powerup_sound = pygame.mixer.Sound('sounds/powerup.wav')
powerup_sound.set_volume(0.25)

power_life_sound = pygame.mixer.Sound('sounds/extra_life.wav')
power_life_sound.set_volume(0.3)

power_bullets_sound = pygame.mixer.Sound('sounds/faster_bullets.wav')
power_bullets_sound.set_volume(0.3)

power_shield_sound = pygame.mixer.Sound('sounds/shield.wav')
power_shield_sound.set_volume(0.3)

power_shrink_sound = pygame.mixer.Sound('sounds/shrink.wav')
power_shrink_sound.set_volume(0.3)

# Play the background music in a loop
pygame.mixer.music.play(loops=-1, start=0.0)  # Loops indefinitely
