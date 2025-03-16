from game_system import GameSystem

def main():
    # Get number of players
    while True:
        try:
            num_players = int(input("How many players? (1-7): "))
            if 1 <= num_players <= 7:
                break
            print("Please enter a number between 1 and 7")
        except ValueError:
            print("Please enter a valid number")

    game = GameSystem(num_players)

    while True:
        game.startGame()

        # Each player takes their turn
        for player_num in range(num_players):
            print(f"\nPlayer {player_num + 1}'s turn")
            print(f"Dealer's face-up card: {game.players[-1].hand.cards[0]}")
            print(f"Your cards: {game.players[player_num].hand.cards}")
            print(f"Your hand value: {game.players[player_num].hand.getValue()}")
            # Player's turn
            while True:
                action = input("\nWhat would you like to do? (hit/stand/double): ").lower()
                if action in ['hit', 'stand', 'double']:
                    game.processAction(game.players[player_num], action)
                    print(f"Your hand: {game.players[player_num].hand.cards}")
                    print(f"Your hand value: {game.players[player_num].hand.getValue()}")

                    if game.players[player_num].hand.isBust():
                        print("Bust!")
                        break
                    if action in ['stand', 'double']:
                        break

        # Dealer's turn
        game.dealerPlay()
        print("\nDealer's final hand:", game.players[-1].hand.cards)
        print("Dealer's hand value:", game.players[-1].hand.getValue())

        # Show results for each player
        for player_num in range(num_players):
            print(f"\nPlayer {player_num + 1}: {game.determineWinner(player_num)}")

        if input("\nPlay again? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()