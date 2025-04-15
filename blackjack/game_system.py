from blackjack.deck import Deck
from blackjack.player import Player
from blackjack.dealer import Dealer
from blackjack.hand import Hand

class GameSystem:
    def __init__(self):
        self.deck = Deck()
        self.players = [Dealer()]
    def add_player(self, player):
        if isinstance(player, Player):  # or just Player, if Dealer isn't supposed to be here
            self.players.append(player)
        else:
            print("Tried to add invalid player:", player, type(player))
    def get_player(self,name):
        for player in self.players:
            if player.name == name:
                return player
    def startGame(self):
        self.deck = Deck()
        for player in self.players:
            player.hand = Hand()
            player.hit(self.deck.drawCard(), player.hand)
            player.hit(self.deck.drawCard(), player.hand)

    def processAction(self, player, action, hand_parameter):
        if action == 'hit':
            player.hit(self.deck.drawCard(), hand_parameter)
        elif action == 'stand':
            player.stand()
        elif action == 'doubleDown':
            player.doubleDown(self.deck.drawCard(), hand_parameter)
        elif action == 'split':
            player.split(self.deck.drawCard(), self.deck.drawCard())

    def determineWinner(self):
        winners_dict = {}
        dealerValue = self.players[0].hand.getValue()
        for player in self.players:
            if player.name == 'dealer':
                continue
            playerValue = player.hand.getValue()
            if(player.busted == True):
                winners_dict[player.playerid] = 'bust'
                continue
            if playerValue > 21:
                winners_dict[player.playerid] = 'bust'
            elif dealerValue > 21 or playerValue > dealerValue:
                winners_dict[player.playerid] = 'winner'
            elif playerValue < dealerValue:
                winners_dict[player.playerid] = 'loser'
            elif playerValue == dealerValue:
                winners_dict[player.playerid] = 'push'
            elif playerValue == 21:
                winners_dict[player.playerid] = 'blackjack'
        return winners_dict
    def dealerPlay(self):
        self.players[0].play(self.deck)
