import unittest
from paylines import Paylines

class TestPaylines(unittest.TestCase):
    
    def setUp(self):
        self.paylines = Paylines()

    def test_get_paylines_five(self):
        expected_five_paylines = [
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Top row
            [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],  # Middle row
            [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],  # Bottom row
            [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)],  # V-shape
            [(0, 2), (1, 1), (2, 0), (3, 1), (4, 2)],  # Caret
        ]
        self.assertEqual(self.paylines.get_paylines_five(), expected_five_paylines)

    def test_get_paylines_three(self):
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

    def test_payline_five_structure(self):
        # Ensure the five-line payline structure contains exactly 5 paylines
        self.assertEqual(len(self.paylines.get_paylines_five()), 5)

        # Ensure each payline in five-paylines has exactly 5 tuples
        for payline in self.paylines.get_paylines_five():
            self.assertEqual(len(payline), 5)

    def test_payline_three_structure(self):
        # Ensure the three-line payline structure contains exactly 14 paylines
        self.assertEqual(len(self.paylines.get_paylines_three()), 14)

        # Ensure each payline in three-paylines has exactly 3 tuples
        for payline in self.paylines.get_paylines_three():
            self.assertEqual(len(payline), 3)
    
if __name__ == '__main__':
    unittest.main()
