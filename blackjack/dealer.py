from player import Player

# The Dealer class inherits from the Player class
class Dealer(Player):
    def __init__(self):
        # Call the constructor of the parent class
        super().__init__()

    def play(self, deck):
        # The dealer must hit until their hand value is at least 17 (Blackjack rules)
        while self.hand.getValue() < 17:
            self.hit(deck.drawCard(), self.hand)