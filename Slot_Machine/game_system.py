from paylines import Paylines
from player import Player
from reels import Reels
from symbols import Symbols
from payouts import Payouts

class GameSystem:
    def __init__(self, player): # initialize objects for all needed classes
        self.symbols = Symbols()
        self.player = player
        self.reels = Reels(self.symbols.symbols)
        self.paylines = Paylines()
        self.payouts = Payouts()

    def start_game(self):
        self.player.current_bet = 0
        self.player.balance = 1000

    def spin_reels(self): 
        if self.player.current_bet == 0:
            raise ValueError("Enter a bet")
        
        result = self.reels.spin()
        return result
        
    def determine_payout(self, result): 
        # pass spin_reels result into determine_win and check paylines
        winning_info = self.payouts.determine_win(result, self.paylines)
        total_payout = 0

        # if there is a winning result
        if winning_info["five_winning_symbol"] is not None:
            # pass that symbol into determine_payouts and return the appropriate payout
            total_payout = self.payouts.determine_payout(winning_info["five_winning_symbol"], 5, self.player)

        if winning_info["three_winning_symbol"] is not None:
            # pass that symbol into determine_payouts and return the appropriate payout
            total_payout = self.payouts.determine_payout(winning_info["three_winning_symbol"], 3, self.player)

        if winning_info["special_symbol_found"]:
            total_payout += self.payouts.determine_special_payout(self.player)

        return total_payout