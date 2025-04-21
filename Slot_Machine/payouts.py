from player import Player

class Payouts:
    def __init__(self):
        #payout multiplier
        self.symbol_payouts = {
            '🍒': {3: 2, 5: 5},        
            '🍋': {3: 3, 5: 8},        
            '🍉': {3: 4, 5: 12},  
            '🍊': {3: 5, 5: 15},
            '🍓': {3: 6, 5: 18},       
            '🔔': {3: 10, 5: 30},       
            '💎': {3: 30, 5: 100},       
            '🌟': {3: 100, 5: 500},      
            }
        
    def determine_win(self, result, paylines):
        five_winning_symbol = None
        three_winning_symbol = None
        special_symbol_found = False
        special_symbol = '🎲'

        special_symbol_count = [symbol for row in result for symbol in row]
        if special_symbol_count.count(special_symbol) >= 3:
            special_symbol_found = True

        for line in paylines.get_paylines_five():
            symbols_on_line = [result[col][row] for col, row in line]
            if all(symbol == symbols_on_line[0] for symbol in symbols_on_line):
                five_winning_symbol = symbols_on_line[0]
                break  # Stop early if we find a 5-match
        
        if not five_winning_symbol:
            for line in paylines.get_paylines_three():
                symbols_on_line = [result[col][row] for col, row in line]
                if all(symbol == symbols_on_line[0] for symbol in symbols_on_line):
                    three_winning_symbol = symbols_on_line[0]
                    break

        return {
            "five_winning_symbol": five_winning_symbol,
            "three_winning_symbol": three_winning_symbol,
            "special_symbol_found": special_symbol_found
        }
    
    def determine_payout(self, winning_symbol, count, player):
        if player.current_bet > 0:
            if winning_symbol in self.symbol_payouts and count in self.symbol_payouts[winning_symbol]:
                payout = player.current_bet * self.symbol_payouts[winning_symbol][count]
                player.win_payout(payout)
                return payout
        return 0
    
    def determine_special_payout(self, player):
        bonus_amount = 100
        player.win_payout(bonus_amount)

        return bonus_amount