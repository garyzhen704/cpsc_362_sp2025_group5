import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(self.height)] #1 represent walls

    def generate_maze(self):
        self.maze = [[1 for _ in range[self.width]] for _ in range(self.height)]
        
        start_x, start_y = 1,1
        self.maze[start_x][start_y] = 0 #mark as path

        #recursive backtrack to gen maze
        self._carve_passages[start_x, start_y]

        #create entrance and exit
        self.maze[0][1] = 0 #entrance at top
        self.maze[self.height-1][self.width-2]

        return self.maze