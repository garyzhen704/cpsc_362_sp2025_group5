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

    def move_player(self,direction):
        #up,down,left,right
        success = self.player.move(direction, self.maze)

        #check if player reached end
        player_pos = self.player.get_position()
        if player_pos[0] == self.end_pos[0] and player_pos[1] == self.end_pos[1]:
            self.completed = True

        return {
            'success': success,
            'position': player_pos,
            'moves': self.player.moves,
            'completed': self.completed,
            'level': self.level
        }

    def generate_new_level(self):
        """Generate a new maze level"""
        self.level += 1
        self.maze = self.generator.generate_maze()
        start_pos = self.generator.get_start_position()
        self.player.reset(start_pos[0], start_pos[1])
        self.end_pos = self.generator.get_end_position()
        self.completed = False
        
        return {
            'maze': self.maze,
            'position': self.player.get_position(),
            'moves': self.player.moves,
            'completed': self.completed,
            'level': self.level
        }
    
    def get_game_state(self):
        """Return the current game state"""
        return {
            'maze': self.maze,
            'position': self.player.get_position(),
            'moves': self.player.moves,
            'completed': self.completed,
            'level': self.level
        }