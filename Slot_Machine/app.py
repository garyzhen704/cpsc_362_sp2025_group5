from flask import Flask, request, jsonify, render_template, Blueprint
from Slot_Machine.player import Player
from Slot_Machine.game_system import GameSystem

slot_bp = Blueprint('slot', __name__, template_folder='templates', static_folder='static')

player = Player()
game_system = GameSystem(player)

@slot_bp.route('/')
def slot_home():
    return render_template('slot_display.html')


@slot_bp.route('/start', methods=['POST'])
def start_game():
    game_system.start_game()

    return jsonify({
        'balance': player.check_balance(),
        'current_bet': player.current_bet
    })

@slot_bp.route('/place_bet', methods=['POST'])
def place_bet():
    data = request.get_json()  
    bet_amount = data.get('bet_amount', 0)

    success = player.place_bet(bet_amount)

    return jsonify({
        'success': success,
        'balance': player.balance,
        'current_bet': player.current_bet
    })

@slot_bp.route("/spin", methods=["POST"])
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