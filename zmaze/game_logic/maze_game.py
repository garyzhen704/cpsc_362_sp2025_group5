from models.maze_generator import MazeGenerator
from models.player import MazePlayer

class MazeGame:
    def __init__(self,width=21,height=21):
        self.width = width
        self.height = height
        self.generator = MazeGenerator(width,height)
        self.maze = self.generator.generate_maze()

        #init player start pos
        start_pos = self.generator.get_start_pos()
        self.player = MazePlayer(start_pos[0],start_pos[1])

        self.end_pos = self.generator.get_end_pos()
        self.completed = False
        self.level = 1
        