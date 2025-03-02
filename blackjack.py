# test.py - Simple Blackjack card test
class Card:
    def __init__(self, value):
        self.value=value  # Missing space around = (linting issue)

card = Card("Ace")
print(card.value)


#Player action and Dealer - Gary
class Player:
    def __init__(self, game, balance=100):
        self.game = game
        self.hand = []
        self.balance = balance
        self.bet = 0

class Dealer:
    def __init__(self, game):
        self.game = game
        self.hand = []
