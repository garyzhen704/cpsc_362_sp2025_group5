class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # represents the card as a "rank of suit"
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    
    # creates a dictionary from a Card object
    def to_dict(self):
        return {'rank': self.rank, 'suit': self.suit}

    # creates a Card object from a dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(data['rank'], data['suit'])