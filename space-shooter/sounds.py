import pygame

# Initialize mixer for sound
pygame.mixer.init()

# Load sound effects and music
shooting_sound = pygame.mixer.Sound('space-shooter/sounds/bullet_shot.mp3')  # Path to sound file
death_sound = pygame.mixer.Sound('space-shooter/sounds/player_death.mp3')
asteroid_exp_sounds = [
    pygame.mixer.Sound('space-shooter/sounds/asteroid_explode1.mp3'),
    pygame.mixer.Sound('space-shooter/sounds/asteroid_explode2.mp3'),
    pygame.mixer.Sound('space-shooter/sounds/asteroid_explode3.mp3'),
]
pygame.mixer.music.load('space-shooter/sounds/background_sd.mp3')

# Set default volume for all sounds
shooting_sound.set_volume(0.06)
death_sound.set_volume(0.6)
for sound in asteroid_exp_sounds:
    sound.set_volume(0.5)

# Set background music volume
pygame.mixer.music.set_volume(0.2)

# Play the background music in a loop
pygame.mixer.music.play(loops=-1, start=0.0)  # Loops indefinitely
