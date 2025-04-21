import random
from symbols import Symbols

class Reels:
    def __init__(self, symbols, reel_length=30, reels_count=5, reel_size=3):
        self.symbols = symbols
        self.reels_count = reels_count
        self.reel_size = reel_size
        self.reels = [self.generate_reel(reel_length) for _ in range(self.reels_count)]

    def generate_reel(self, reel_length):
        # Generate a weighted list of symbols for each reel
        weighted_symbols = [symbol for symbol, weight in self.symbols.items() for _ in range(weight)]
        return random.choices(weighted_symbols, k=reel_length)

    def spin(self, num_stops=3):
        result = []
        for reel in self.reels:
            # Randomly pick a start position for the spin
            start = random.randint(0, len(reel) - 1)
            result.append([reel[(start + i) % len(reel)] for i in range(num_stops)])
        return result
