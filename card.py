class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # represents the card as a "rank of suit"
    def __repr__(self):
        return f"{self.rank} of {self.suit}"