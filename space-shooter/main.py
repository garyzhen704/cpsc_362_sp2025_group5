import sys
import pygame
from pygame.locals import *
import globals as gl
from object import Object
from vector import Vector
from player import Player
from asteroid import Asteroid

def wrap(num, min, max):
    range_size = max - min + 1
    return (num - min) % range_size + min

def clamp_to_screen(obj: Object):
    radius = obj.hitbox.radius
    x = wrap(obj.position.x, -radius, gl.screen_width + radius)
    y = wrap(obj.position.y, -radius, gl.screen_height + radius)
    obj.position = Vector(x, y)

pygame.init()
screen = pygame.display.set_mode((gl.screen_width, gl.screen_height))
pygame.display.set_caption("Space Shooter")
fps_clock = pygame.time.Clock()

player = Player(gl.player_start_pos, gl.WHITE)
gl.spawn_obj(player)

test_asteroid = Asteroid(5, Vector(500, 500), Vector(-400, 200))
gl.spawn_obj(test_asteroid)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #debug
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                for obj in gl.game_objects.copy():
                    if isinstance(obj, Asteroid):
                        obj.destroy()

    screen.fill(gl.BLACK)

    # Update and draw every object
    obj: Object
    for obj in gl.game_objects:
        obj.update(gl.FPS)
        clamp_to_screen(obj)
        obj.draw(screen)

    pygame.display.update()

    fps_clock.tick(gl.FPS)
