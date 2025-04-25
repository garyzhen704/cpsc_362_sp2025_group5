class Player:
    def __init__(self, balance=1000):
        self.balance = balance
        self.current_bet = 0  

    def place_bet(self, amount): # place bet if player has enough funds 
        if amount <= self.balance and amount > 0:
            self.current_bet = amount  
            return True
        else:
            raise ValueError("Insufficient funds or invalid bet amount")

    def deduct_bet(self): # only deduct bet if player has enolugh funds 
        if self.current_bet > 0 and self.current_bet <= self.balance:
            self.balance -= self.current_bet
            return True
        return False
    
    def win_payout(self, payout): # pass payout results back and update balance 
        self.balance += payout

    def check_balance(self): # return player balance 
        return self.balance
