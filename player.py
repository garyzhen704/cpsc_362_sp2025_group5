from hand import Hand

class Player:
    def __init__(self, balance=100):
        self.balance = balance
        self.hand = Hand()
        self.second_hand = Hand()
        self.currentBet = 0

    def hit(self, card, hand_parameter):
        hand_parameter.addCard(card)

    def stand(self):
        pass

    def placeBet(self, amount):
        if amount <= self.balance:
            self.currentBet = amount
            self.balance -= amount
            return True
        return False

    def doubleDown(self, card, hand_parameter):
        if self.canDoubleDown():
            self.balance -= self.currentBet
            self.currentBet *= 2
            hand_parameter.addCard(card)
            return True
        else:
            return False

    def split(self, card1, card2):
        if self.canSplit():
            self.second_hand.addCard(self.hand.cards.pop())
            self.hand.addCard(card1)
            self.second_hand.addCard(card2)
            return True
        else:
            return False

    def canSplit(self):
        if(len(self.hand.cards) == 2 and self.hand.cards[0].rank == self.hand.cards[1].rank):
            return True
    def canDoubleDown(self, hand_parameter):
        if(len(hand_parameter.cards) == 2 and self.balance >= self.currentBet):
            return True
        else:
            return False
