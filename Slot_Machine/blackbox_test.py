import unittest
from paylines import Paylines


class TestPaylinesBlackBox(unittest.TestCase):
    
    def setUp(self):
        self.paylines = Paylines()

    def test_get_paylines_five_valid(self):
        # Verify that the method returns the expected paylines
        expected_five_paylines = [
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Top row
            [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],  # Middle row
            [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],  # Bottom row
            [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)],  # V-shape
            [(0, 2), (1, 1), (2, 0), (3, 1), (4, 2)],  # Caret
        ]
        self.assertEqual(self.paylines.get_paylines_five(), expected_five_paylines)
    
    def test_get_paylines_three_valid(self):
        # Verify that the method returns the expected paylines
        expected_three_paylines = [
            # columns
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(3, 0), (3, 1), (3, 2)],
            [(4, 0), (4, 1), (4, 2)],

            # rows
            [(0, 0), (1, 0), (2, 0)], [(1, 0), (2, 0), (3, 0)], [(2, 0), (3, 0), (4, 0)],
            [(0, 1), (1, 1), (2, 1)], [(1, 1), (2, 1), (3, 1)], [(2, 1), (3, 1), (4, 1)],
            [(0, 2), (1, 2), (2, 2)], [(1, 2), (2, 2), (3, 2)], [(2, 2), (3, 2), (4, 2)],
        ]
        self.assertEqual(self.paylines.get_paylines_three(), expected_three_paylines)

    def test_get_paylines_five_empty(self):
        # Check for an empty case 
        self.paylines.paylines_five = [] 
        self.assertEqual(self.paylines.get_paylines_five(), [])

    def test_get_paylines_three_empty(self):
        # Check for an empty case 
        self.paylines.paylines_three = [] 
        self.assertEqual(self.paylines.get_paylines_three(), [])

    def test_get_paylines_five_structure(self):
        # Test the structure 
        result = self.paylines.get_paylines_five()
        for payline in result:
            self.assertEqual(len(payline), 5)
    
    def test_get_paylines_three_structure(self):
        # Test the structure 
        result = self.paylines.get_paylines_three()
        for payline in result:
            self.assertEqual(len(payline), 3)

if __name__ == '__main__':
    unittest.main()
