from flask import Flask, render_template, url_for, jsonify, request
from game_system import GameSystem
from card import Card
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('example.html')
game_system = GameSystem()
@app.route('/start', methods=['POST'])
def start_game():
    # Start a new game
    game_system.startGame()
    dealer_hand = game_system.players[1].hand.cards
    dealer_hand[1].is_face_down = True  # Face down the second card

    player_hand = [card.to_dict() for card in game_system.players[0].hand.cards]
    dealer_hand = [card.to_dict() for card in game_system.players[1].hand.cards]
    return jsonify({
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'deck': [card.to_dict() for card in game_system.deck.cards],
        'player_value': game_system.players[0].hand.getValue()
    })
    
@app.route('/hit', methods=['POST'])
def hit():
    # Handle the player's "hit" action
    data = request.json
    #print("The size of deck " +str(len(game_system.deck.cards)))
    #game_system.deck.cards = [Card.from_dict(card) for card in data['deck']]
    #print("The size of deck " +str(len(game_system.deck.cards)))
    game_system.players[0].hand.cards = [Card.from_dict(card) for card in data['player_hand']]
    #print("The size of deck " +str(len(game_system.deck.cards)))
    game_system.processAction(game_system.players[0], 'hit', game_system.players[0].hand)
    player_hand = [card.to_dict() for card in game_system.players[0].hand.cards]
    return jsonify({
        'player_hand': player_hand,
        'deck': [card.to_dict() for card in game_system.deck.cards],
        'player_value': game_system.players[0].hand.getValue()
    })

@app.route('/stand', methods=['POST'])
def stand():
    # Handle the player's "stand" action
    data = request.json 
    #print(data['deck'])
    #game_system.deck.cards = [Card.from_dict(card) for card in data['deck']]
    print(game_system.players[0].hand.cards)
    game_system.players[0].hand.cards = [Card.from_dict(card) for card in data['player_hand']]
    print(game_system.players[0].hand.cards)
    print(game_system.players[1].hand.cards)
    print(data['dealer_hand'])
    game_system.players[1].hand.cards = [Card.from_dict(card) for card in data['dealer_hand']]
    print(game_system.players[1].hand.cards)

    game_system.processAction(game_system.players[0], 'stand', game_system.players[0].hand)
    game_system.dealerPlay()
    dealer_hand = [card.to_dict() for card in game_system.players[1].hand.cards]
    return jsonify({
        'dealer_hand': dealer_hand,
        'dealer_value': game_system.players[1].hand.getValue(),
        'player_value': game_system.players[0].hand.getValue(),
        'result': game_system.determineWinner()
    })

if __name__ == '__main__':
  app.run(debug = True)