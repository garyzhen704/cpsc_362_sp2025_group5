class MazePlayer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moves = 0

    def get_position(self):
        return (self.x, self.y)
    
    def move(self, direction, maze):
        #move player in specified direction

        new_x, new_y = self.x, self.y

        if direction == 'up':
            new_y -= 1
        elif direction == 'down':
            new_y += 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1
        
        #check if valid move
        if (0 <= new_y < len(maze) and
            0 <= new_x < len(maze[0]) and
            maze[new_y][new_x] == 0):

            self.x, self.y = new_x, new_y
            self.moves += 1
            return True
        
        return False
    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.moves = 0

    def set_position(self,x,y): ## added for testing whitebox
        self.x = x
        self.y = y