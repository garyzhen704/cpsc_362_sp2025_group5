import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(self.height)] #1 represent walls

    def generate_maze(self):
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = 0  # mark as path

        # recursive backtrack to gen maze
        self._carve_passages(start_x, start_y)

        # create entrance and exit
        self.maze[0][1] = 0  # entrance at top
        self.maze[self.height-1][self.width-2] = 0

        return self.maze
    
    def _carve_passages(self, x, y):
        # directions - up, right, down, left
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # check if new cell is within bounds
            if 0 < nx < self.width-1 and 0 < ny < self.height-1 and self.maze[ny][nx] == 1:
                self.maze[y+dy//2][x+dx//2] = 0  # creates path between cells
                self.maze[ny][nx] = 0
                self._carve_passages(nx, ny)

    def get_start_pos(self):
        return(1,0)
    
    def get_end_pos(self):
        return(self.width-2, self.height-1)
    
    def print_maze(self):
        for row in self.maze:
            print(''.join(['#' if cell == 1 else '' for cell in row]))

    