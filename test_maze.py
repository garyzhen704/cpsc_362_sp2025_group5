# test_maze.py (place in project root, same level as app.py)
import unittest
from zmaze.models.maze_generator import MazeGenerator
from zmaze.models.player import MazePlayer
from zmaze.game_logic.maze_game import MazeGame

class TestMazeGame(unittest.TestCase):
    
    def setUp(self):
        # Create test objects before each test
        self.maze_generator = MazeGenerator(21, 21)
        self.maze = self.maze_generator.generate_maze()
        self.game = MazeGame(21, 21)
    
    def test_maze_generation(self):
        # Test that maze is generated with correct dimensions
        self.assertEqual(len(self.maze), 21)
        self.assertEqual(len(self.maze[0]), 21)
        
        # Test that entrance and exit exist
        self.assertEqual(self.maze[0][1], 0)  # Entrance
        self.assertEqual(self.maze[20][19], 0)  # Exit
    
    def test_player_movement(self):
        # Test valid moves
        player = MazePlayer(1, 1)
        self.maze[1][1] = 0  # Current position is path
        self.maze[1][2] = 0  # Right is path
        
        # Valid move
        result = player.move("right", self.maze)
        self.assertTrue(result)
        self.assertEqual(player.get_position(), (2, 1))
        self.assertEqual(player.moves, 1)
        
        # Invalid move (into wall)
        self.maze[1][3] = 1  # Wall to the right
        result = player.move("right", self.maze)
        self.assertFalse(result)
        self.assertEqual(player.get_position(), (2, 1))  # Position unchanged
        self.assertEqual(player.moves, 1)  # Moves unchanged
    
    def test_game_completion(self):
        # Test game completion when player reaches end
        self.game.player.set_position(19, 19)  # Near the exit
        
        # Move to exit
        result = self.game.move_player("down")
        
        # Check game is completed
        self.assertTrue(result["completed"])
        self.assertEqual(result["moves"], 1)
    
    def test_new_level_generation(self):
        # Test level progression
        initial_level = self.game.level
        initial_maze = self.game.maze
        
        # Generate new level
        new_state = self.game.generate_new_level()
        
        # Check level incremented
        self.assertEqual(new_state["level"], initial_level + 1)
        self.assertEqual(self.game.player.moves, 0)  # Moves reset
        self.assertFalse(new_state["completed"])  # Not completed

if __name__ == '__main__':
    unittest.main()
