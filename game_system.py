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
        # Clear hands
        for player in self.players:
            player.hand = Hand()

        # Deal first card face up to all players
        for player in self.players:
            player.hit(self.deck.drawCard())

        # Deal second card (face up to player, face down to dealer)
        self.players[0].hit(self.deck.drawCard())  # Player's second card
        self.players[1].hit(self.deck.drawCard())  # Dealer's hidden card

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