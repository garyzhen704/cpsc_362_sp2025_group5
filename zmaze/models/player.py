class MazePlayer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moves = 0

    def get_position(self):
        return (self.x, self.y)