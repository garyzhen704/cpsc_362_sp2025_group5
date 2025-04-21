from collections import Counter
from reels import Reels
from paylines import Paylines
from payouts import Payouts
from symbols import Symbols

# Initialize all components
symbols = Symbols().get_symbols()
reels = Reels(symbols)
paylines = Paylines()
payouts = Payouts()

# Run simulation
wins = 0
special = 0
trials = 100

for _ in range(trials):
    result = reels.spin()
    winning_info = payouts.determine_win(result, paylines)

    if winning_info["five_winning_symbol"] is not None:
        wins += 1
    if winning_info["three_winning_symbol"] is not None:
        wins += 1
    if winning_info["special_symbol_found"]:
        special += 1
print(f"Win rate over {trials} spins: {wins} Wins, {special} Special")
