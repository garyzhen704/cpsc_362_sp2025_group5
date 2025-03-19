from flask import Flask, render_template, url_for, jsonify, request
from game_system import GameSystem
from card import Card
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('example.html')

game_system = GameSystem()

@app.route('/place_bet', methods=['POST'])
def place_bet():
    # Handle bet placement
    data = request.json
    bet_amount = int(data['bet_amount'])
    player = game_system.players[0]
    
    # Place the bet
    success = player.placeBet(bet_amount)
    
    return jsonify({
        'success': success,
        'balance': player.balance,
        'current_bet': player.currentBet
    })

@app.route('/cancel_bet', methods=['POST'])
def cancel_bet():
    # Return the bet to the player's balance
    player = game_system.players[0]
    player.balance += player.currentBet
    player.currentBet = 0
    
    return jsonify({
        'success': True,
        'balance': player.balance,
        'current_bet': player.currentBet
    })

@app.route('/reset_balance', methods=['POST'])
def reset_balance():
    # Reset the player's balance to 100
    player = game_system.players[0]
    player.balance = 100
    player.currentBet = 0
    
    return jsonify({
        'success': True,
        'balance': player.balance,
        'current_bet': player.currentBet
    })

@app.route('/start', methods=['POST'])
def start_game():
    # Start a new game
    game_system.startGame()
    dealer_hand = game_system.players[1].hand.cards
    dealer_hand[1].is_face_down = True  # Face down the second card

    player = game_system.players[0]
    player_hand = [card.to_dict() for card in player.hand.cards]
    dealer_hand = [card.to_dict() for card in dealer_hand]
    
    # Check if double down is possible
    can_double_down = player.canDoubleDown(player.hand)
    
    return jsonify({
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'player_value': player.hand.getValue(),
        'can_double_down': can_double_down,
        'balance': player.balance,
        'current_bet': player.currentBet
    })
    
@app.route('/hit', methods=['POST'])
def hit():
    # Handle the player's "hit" action
    data = request.json
    player = game_system.players[0]
    
    # Update player hand from frontend
    player.hand.cards = [Card.from_dict(card) for card in data['player_hand']]
    
    # Process hit action
    game_system.processAction(player, 'hit', player.hand)
    player_hand = [card.to_dict() for card in player.hand.cards]
    player_value = player.hand.getValue()
    
    response_data = {
        'player_hand': player_hand,
        'player_value': player_value,
        'balance': player.balance,
        'current_bet': player.currentBet
    }
    
    # If player busts, process as a loss
    if player_value > 21:
        # Reset bet since player lost
        player.currentBet = 0
        response_data['balance'] = player.balance
        response_data['current_bet'] = player.currentBet
    
    return jsonify(response_data)

@app.route('/stand', methods=['POST'])
def stand():
    # Handle the player's "stand" action
    data = request.json
    player = game_system.players[0]
    dealer = game_system.players[1]
    
    # Update hands from frontend
    player.hand.cards = [Card.from_dict(card) for card in data['player_hand']]
    dealer.hand.cards = [Card.from_dict(card) for card in data['dealer_hand']]

    # Process stand action
    game_system.processAction(player, 'stand', player.hand)
    game_system.dealerPlay()
    
    # Get the winner
    result = game_system.determineWinner()
    
    # Process bet payout
    if "Player wins" in result:
        player.balance += player.currentBet * 2  # Return bet + winnings
    elif "tie" in result:
        player.balance += player.currentBet  # Return bet
    
    # Reset current bet after payout
    current_bet = player.currentBet
    player.currentBet = 0
    
    dealer_hand = [card.to_dict() for card in dealer.hand.cards]
    return jsonify({
        'dealer_hand': dealer_hand,
        'dealer_value': dealer.hand.getValue(),
        'player_value': player.hand.getValue(),
        'result': result,
        'balance': player.balance,
        'current_bet': player.currentBet
    })

@app.route('/double_down', methods=['POST'])
def double_down():
    # Handle the player's double down action
    data = request.json
    player = game_system.players[0]
    dealer = game_system.players[1]
    
    # Update hands from frontend
    player.hand.cards = [Card.from_dict(card) for card in data['player_hand']]
    dealer.hand.cards = [Card.from_dict(card) for card in data['dealer_hand']]

    # Process double down action
    game_system.processAction(player, 'doubleDown', player.hand)
    
    # After double down, dealer plays and game completes
    game_system.dealerPlay()
    
    # Get the winner
    result = game_system.determineWinner()
    
    # Process bet payout
    if "Player wins" in result:
        player.balance += player.currentBet * 2  # Return bet + winnings
    elif "tie" in result:
        player.balance += player.currentBet  # Return bet
    
    # Reset current bet after payout
    current_bet = player.currentBet
    player.currentBet = 0
    
    player_hand = [card.to_dict() for card in player.hand.cards]
    dealer_hand = [card.to_dict() for card in dealer.hand.cards]
    
    return jsonify({
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'player_value': player.hand.getValue(),
        'dealer_value': dealer.hand.getValue(),
        'result': result,
        'balance': player.balance,
        'current_bet': current_bet
    })

if __name__ == '__main__':
  app.run(debug = True)