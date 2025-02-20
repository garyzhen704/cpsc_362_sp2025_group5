# test.py - Simple Blackjack card test
class Card:
    def __init__(self, value):
        self.value=value  # Missing space around = (linting issue)

card = Card("Ace")
print(card.value)