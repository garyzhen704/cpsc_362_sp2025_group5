from hand import Hand
import random

class Player:
    def __init__(self, balance=100):
        self.name = "no name"
        self.balance = balance
        self.hand = Hand()
        self.second_hand = Hand()
        self.currentBet = 0
        self.status = ""
        self.playerid = str(random.randint(1000, 9999))
        self.turn = False
        self.busted = False
        self.result = ''
        self.adjusted_balance = False
        self.islast = False
    def setName(self,name):
        self.name = name
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
        if self.canDoubleDown(hand_parameter):
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
        if(len(hand_parameter.cards) == 2 and self.balance >= 2*self.currentBet):
            return True
        else:
            return False
