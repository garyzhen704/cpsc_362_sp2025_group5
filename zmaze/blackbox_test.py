import unittest
from models.player import MazePlayer
# Testing the player movement input outputs
#
class TestMazePlayer(unittest.TestCase):

    def setUp(self):
        # This runs before each test method
        self.player = MazePlayer(1, 1)  # Example starting position

    def test_initial_position_and_moves(self):
        # Test the player's initial position and move count
        self.assertEqual(self.player.get_position(), (1, 1))
        self.assertEqual(self.player.moves, 0)

    def test_move_not_valid(self):
        # Simulate a valid move (moving right)
        maze = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        
        # Player moves right
        result = self.player.move('right', maze)
        
        # After moving right, player position should change
        self.assertFalse(result)
        self.assertEqual(self.player.get_position(), (1, 1))
        self.assertEqual(self.player.moves, 0)

    def test_move_valid(self):
        # Simulate a valid move (moving right)
        maze = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 0, 1]
        ]
        
        # Player moves right
        result = self.player.move('down', maze)
        
        # After moving right, player position should change
        self.assertTrue(result)
        self.assertEqual(self.player.get_position(), (1, 2))
        self.assertEqual(self.player.moves, 1)


      
if __name__ == '__main__':
    unittest.main()