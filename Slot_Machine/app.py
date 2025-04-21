from flask import Flask, request, jsonify, render_template
from player import Player
from game_system import GameSystem

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('slot_display.html')

player = Player()
game_system = GameSystem(player)

@app.route('/start', methods=['POST'])
def start_game():
    game_system.start_game()

    return jsonify({
        'balance': player.check_balance(),
        'current_bet': player.current_bet
    })

@app.route('/place_bet', methods=['POST'])
def place_bet():
    data = request.get_json()  # This reads the JSON data from the body
    bet_amount = data.get('bet_amount', 0)

    success = player.place_bet(bet_amount)

    return jsonify({
        'success': success,
        'balance': player.balance,
        'current_bet': player.current_bet
    })

@app.route("/spin", methods=["POST"])
def spin():
    # Spin the reels and determine the result
    result = game_system.spin_reels()

    player.deduct_bet()

    if result != 'Not a Winner':
        payout = game_system.determine_payout(result)


    # Return the updated game state
    return jsonify({
        'result': result,
        'payout': payout,
        'balance': player.check_balance(),
    })

if __name__ == "__main__":
    app.run(debug=True)