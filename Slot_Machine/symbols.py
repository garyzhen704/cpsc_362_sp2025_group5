class Symbols:
    def __init__(self):
        # Defined symbols and the weight(freq) they appear
        self.symbols = {
            '🍒': 500,        
            '🍋': 400,        
            '🍉': 350,   
            '🍊': 300,
            '🍓': 250,         
            '🔔': 150,        
            '💎': 50,         
            '🌟': 20,
            '🎲': 50	         
            }

    def get_symbols(self):
        return self.symbols