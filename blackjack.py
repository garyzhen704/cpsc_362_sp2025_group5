from game_system import GameSystem

def main():
    game = GameSystem()

    while True:
        game.startGame()

        # Show initial hands (dealer's second card is hidden)
        print("\nDealer's face-up card:", game.players[1].hand.cards[0])
        print("Your cards:", game.players[0].hand.cards)
        print("Your hand value:", game.players[0].hand.getValue())

        # Player's turn
        while True:
            action = input("\nWhat would you like to do? (hit/stand/double): ").lower()
            if action in ['hit', 'stand', 'double']:
                game.processAction(game.players[0], action)
                print("Your hand:", game.players[0].hand.cards)
                print("Your hand value:", game.players[0].hand.getValue())

                if game.players[0].hand.isBust():
                    print("Bust!")
                    break
                if action in ['stand', 'double']:
                    break

        # Dealer's turn
        game.dealerPlay()
        print("\nDealer's final hand:", game.players[1].hand.cards)
        print("Dealer's hand value:", game.players[1].hand.getValue())

        # Show result
        print("\n" + game.determineWinner())

        # Ask for new game
        if input("\nPlay again? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()