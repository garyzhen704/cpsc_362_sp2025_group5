class Balance:
    DEFAULT_BALANCE = 100

    def __init__(self):
        self.player_balances = [Balance.DEFAULT_BALANCE]

    # Call at the end of every game
    # Player numbers are 0-indexed
    def save_balance(self, player_num, new_balance):
        if player_num < len(self.player_balances):
            print(f"Saved ${self.player_balances[player_num]} -> ${new_balance} to player {player_num}")
            self.player_balances[player_num] = new_balance
        else:
            print(f"Player {player_num} balance does not exist, could not save")

    def reset_balances(self, remove_players = False):
        if remove_players:
            self.player_balances = [Balance.DEFAULT_BALANCE]
        else:
            for i in range(len(self.player_balances)):
                self.player_balances[i] = Balance.DEFAULT_BALANCE
        print("Reset balance")

    def add_player(self):
        self.player_balances.append(Balance.DEFAULT_BALANCE)
    
    def remove_player(self, player_num = -1):
        self.player_balances.pop(player_num)
