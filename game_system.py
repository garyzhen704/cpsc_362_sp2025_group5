from deck import Deck
from player import Player
from dealer import Dealer
from hand import Hand

class GameSystem:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player(), Dealer()]  # Player and Dealer

    def startGame(self):
        self.deck = Deck()
        for player in self.players:
            player.hand = Hand()
            player.hit(self.deck.drawCard())
            player.hit(self.deck.drawCard())

    def processAction(self, player, action):
        if action == 'hit':
            player.hit(self.deck.drawCard())
        elif action == 'stand':
            player.stand()
        elif action == 'doubleDown':
            player.doubleDown(self.deck.drawCard())

    def determineWinner(self):
        playerValue = self.players[0].hand.getValue()
        dealerValue = self.players[1].hand.getValue()
        if playerValue > 21:
            return "Dealer wins!"
        elif dealerValue > 21 or playerValue > dealerValue:
            return "Player wins!"
        elif playerValue < dealerValue:
            return "Dealer wins!"
        else:
            return "It's a tie!"

    def dealerPlay(self):
        self.players[1].play(self.deck)