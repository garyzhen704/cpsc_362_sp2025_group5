import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in ['hearts', 'diamonds', 'clubs', 'spades']
                      for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        if len(self.cards) == 0:
            print("Deck is empty")  # Handle empty deck
            return None 
        return self.cards.pop()