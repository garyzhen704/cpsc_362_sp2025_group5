from deck import Deck
from player import Player
from dealer import Dealer
from hand import Hand

class GameSystem:
    def __init__(self, num_players):
        self.deck = Deck()
        self.players = [Player() for _ in range(num_players)]
        self.players.append(Dealer())  # Dealer is always last

    def startGame(self):
        self.deck = Deck()
        # Clear hands
        for player in self.players:
            player.hand = Hand()

        # Deal first card face up to all players
        for player in self.players:
            player.hit(self.deck.drawCard(), player.hand)

        # Deal second card (face up to player, face down to dealer)
        for i, player in enumerate(self.players[:-1]):
            player.hit(self.deck.drawCard(), player.hand)  # Players' second cards
        self.players[-1].hit(self.deck.drawCard(), self.players[-1].hand)  # Dealer's hidden card

    def processAction(self, player, action, hand_paramater):
        if action == 'hit':
            player.hit(self.deck.drawCard(), hand_paramater)
        elif action == 'stand':
            player.stand()
        elif action == 'doubleDown':
            player.doubleDown(self.deck.drawCard(), hand_paramater)
        elif action == 'split':
            player.split(self.deck.drawCard(), self.deck.drawCard())

    def determineWinner(self, player_index):
        playerValue = self.players[player_index].hand.getValue()
        dealerValue = self.players[-1].hand.getValue()  # Dealer is last player
        if playerValue > 21:
            return "Dealer wins!"
        elif dealerValue > 21 or playerValue > dealerValue:
            return "Player wins!"
        elif playerValue < dealerValue:
            return "Dealer wins!"
        else:
            return "It's a tie!"
    def dealerPlay(self):
        self.players[-1].play(self.deck)
