class Paylines:
    def __init__(self):
        # win with 5 in a row
        self.paylines_five = [
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Top row
            [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],  # Middle row
            [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],  # Bottom row

            [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)],  # V-shape
            [(0, 2), (1, 1), (2, 0), (3, 1), (4, 2)],
          ]  # Caret

        # Win with 3 in a row
        self.paylines_three = [
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
    
    def get_paylines_five(self):
        return self.paylines_five
    
    def get_paylines_three(self):
        return self.paylines_three