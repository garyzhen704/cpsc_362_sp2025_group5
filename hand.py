from card import Card

class Hand:
    def __init__(self):
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)

    # Calculate the value of the hand
    def getValue(self):
        value = 0
        numAces = 0
        cardValues = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11
        }
        for card in self.cards:
            value += cardValues[card.rank]
            if card.rank == 'A':
                numAces += 1

        # Change the value of the aces to 1 if the hand is over 21        
        while value > 21 and numAces:
            value -= 10
            numAces -= 1
        return value
    def canSplit(self):
        if(len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank):
            return True
    
    def clearHand(self):
        self.cards.clear()


    def isBlackjack(self):
        return self.getValue() == 21 and len(self.cards) == 2

    def isBust(self):
        return self.getValue() > 21