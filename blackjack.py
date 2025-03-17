from game_system import GameSystem

def main():
    evaluate_second_hand = False
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
                if(evaluate_second_hand != True):
                    if(game.players[player_num].canSplit() and game.players[player_num].canDoubleDown(game.players[player_num].hand)):
                        action = input("\nWhat would you like to do? (hit/stand/double/split): ").lower()
                    elif(game.players[player_num].canSplit() and not game.players[player_num].canDoubleDown(game.players[player_num].hand)):
                        action = input("\nWhat would you like to do? (hit/stand/split): ").lower()
                    elif(not game.players[player_num].canSplit() and game.players[player_num].canDoubleDown(game.players[player_num].hand)):
                        action = input("\nWhat would you like to do? (hit/stand/double): ").lower()
                    else:
                        action = input("\nWhat would you like to do? (hit/stand): ").lower()
                else:
                    if(game.players[player_num].canSplit() and game.players[player_num].canDoubleDown(game.players[player_num].second_hand)):
                        action = input("\nWhat would you like to do? (hit/stand/double/split): ").lower()
                    elif(game.players[player_num].canSplit() and not game.players[player_num].canDoubleDown(game.players[player_num].second_hand)):
                        action = input("\nWhat would you like to do? (hit/stand/split): ").lower()
                    elif(not game.players[player_num].canSplit() and game.players[player_num].canDoubleDown(game.players[player_num].second_hand)):
                        action = input("\nWhat would you like to do? (hit/stand/double): ").lower()
                    else:
                        action = input("\nWhat would you like to do? (hit/stand): ").lower()


                if action in ['hit', 'stand', 'double', 'split']:
                    if action in ['stand']:
                        if(len(game.players[player_num].second_hand.cards) != 0 and evaluate_second_hand ==True):
                            break
                        elif(len(game.players[player_num].second_hand.cards) == 0):
                            break
                        evaluate_second_hand = True
                    if(evaluate_second_hand == False):
                        game.processAction(game.players[player_num], action, game.players[player_num].hand)
                        print(f"Your hand: {game.players[player_num].hand.cards}")
                        print(f"Your hand value: {game.players[player_num].hand.getValue()}")
                    else:
                        game.processAction(game.players[player_num], action, game.players[player_num].second_hand)
                        print(f"Your second hand: {game.players[player_num].second_hand.cards}")
                        print(f"Your second hand value: {game.players[player_num].second_hand.getValue()}")

                    if game.players[player_num].hand.isBust():
                        print("Bust!")
                        
                        if(len(game.players[player_num].second_hand.cards) == 0):
                            break
                        elif(len(game.players[player_num].second_hand.cards) != 0 and evaluate_second_hand == True):
                            break
                        if(len(game.players[player_num].second_hand.cards)!=0):
                            evaluate_second_hand = True
                        print(f"Your second hand: {game.players[player_num].second_hand.cards}")
                        print(f"Your second hand value: {game.players[player_num].second_hand.getValue()}")
                    if action in ['double']:
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