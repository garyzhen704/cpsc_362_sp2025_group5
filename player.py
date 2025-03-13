from hand import Hand

class Player:
    def __init__(self, balance=100):
        self.balance = balance
        self.hand = Hand()

    def hit(self, card):
        self.hand.addCard(card)

    def stand(self):
        pass

    def doubleDown(self, card):
        self.hand.addCard(card)
        self.balance -= 10  # Example bet amount