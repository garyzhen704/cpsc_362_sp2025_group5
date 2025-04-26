import unittest
from game_logic.maze_game import MazeGame

class TestMazeGameWhiteBox_check_level_completion(unittest.TestCase):

    def setUp(self):
        self.game = MazeGame(width=5, height=5)
        # Move the player to the tile right before the end
        end_x, end_y = self.game.end_pos
        self.game.player.set_position(end_x - 1, end_y)
            

    def test_completion_and_level_increment(self):
        # Move player right into the end position
        self.game.move_player('right')

        # Check that the game is marked as completed
        self.assertTrue(self.game.completed, "Game should be marked as completed")

        # Step 3: Generate a new level
        self.game.generate_new_level()

        # Check that level incremented and completed reset
        self.assertEqual(self.game.level, 2, "Level should increment to 2")
        self.assertFalse(self.game.completed, "Game completion should reset for new level")

if __name__ == '__main__':
    unittest.main()

