import random
import globals
from object import Object
from vector import Vector

min_speed = 100.0
max_speed = 300.0
# Controls the random angle of asteroid pieces spawned by destroying an asteroid
piece_max_angle_offset = 75.0
piece_speed_offset = 80.0
# A size of 1 is a radius of this many pixels, a size of 2 is 2x larger, etc
size_to_pixel_ratio = 10

class Asteroid(Object):
    def __init__(self, size: float, pos: Vector, vel: Vector):
        self.size = size
        
        new_vel = vel
        if new_vel.magnitude() < min_speed:
            new_vel = new_vel.normalized() * min_speed
        elif new_vel.magnitude() > max_speed:
            new_vel = new_vel.normalized() * max_speed
        
        super().__init__(size * size_to_pixel_ratio, pos, new_vel, globals.GRAY)

    def destroy(self):
        if self.size > 1:
            # Angle that the first piece will move. Completely random
            angle1 = random.random() * 360.0
            # Angle that the second piece will move. Opposite direction of first piece, plus a random offset
            angle2 = angle1 + 180.0 + random.uniform(-piece_max_angle_offset, piece_max_angle_offset)
            # Spawn a new asteroid with half the size
            self._spawn_piece(self.size // 2, angle1)
            # Spawn another with the remaining size
            self.size -= self.size // 2
            self._spawn_piece(self.size, angle2)
        globals.delete_obj(self)

    def _spawn_piece(self, size, angle):
        # Add random velocity to piece
        vel_add = self.velocity.normalized() * (random.uniform(-piece_speed_offset, piece_speed_offset))
        globals.spawn_obj(Asteroid(size, self.position, (self.velocity + vel_add).rotated(angle)))
