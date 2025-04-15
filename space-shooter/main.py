import sys
import pygame
from pygame.locals import *
import globals as gl
from object import Object
from vector import Vector
from player import Player


def clamp_to_screen(obj: Object):
    obj.position = Vector(obj.position.x % gl.screen_width, obj.position.y % gl.screen_height)


pygame.init()
screen = pygame.display.set_mode((gl.screen_width, gl.screen_height))
pygame.display.set_caption("Space Shooter")
fps_clock = pygame.time.Clock()

player = Player(gl.player_start_pos, gl.WHITE)
gl.spawn_obj(player)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(gl.BLACK)

    # Update and draw every object
    obj: Object
    for obj in gl.game_objects:
        obj.update()
        clamp_to_screen(obj)
        obj.draw(screen)

    pygame.display.update()

    fps_clock.tick(gl.FPS)
