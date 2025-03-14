from hand import Hand

class Player:
    def __init__(self, balance=100):
        self.balance = balance
        self.hand = Hand()
        self.currentBet = 0

    def hit(self, card):
        self.hand.addCard(card)

    def stand(self):
        pass

    def placeBet(self, amount):
        if amount <= self.balance:
            self.currentBet = amount
            self.balance -= amount
            return True
        return False

    def doubleDown(self, card):
        if self.balance >= self.currentBet:
            self.balance -= self.currentBet
            self.currentBet *= 2
        self.hand.addCard(card)
