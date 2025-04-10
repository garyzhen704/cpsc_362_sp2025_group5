from flask import Blueprint, render_template, request, jsonify, session
from game_logic.maze_game import MazeGame

maze_bp = Blueprint('maze', __name__,
                    url_prefix='/maze',
                    template_folder='.../templates',
                    static_folder='../static',
                    static_url_path='/static')

@maze_bp.route('/')
def maze_page():
    #render maze game page
    return render_template('maze.html')

@maze_bp.route('/new-game', methods=['POST'])
def new_game():
    """Start a new maze game"""
    # Create a new game with default size
    game = MazeGame()
    
    # Store game state in session
    session['maze_game'] = {
        'maze': game.maze,
        'player_pos': game.player.get_position(),
        'end_pos': game.end_pos,
        'level': game.level,
        'moves': game.player.moves,
        'completed': game.completed
    }
    
    return jsonify({
        'maze': game.maze,
        'player_pos': game.player.get_position(),
        'end_pos': game.end_pos,
        'level': game.level,
        'moves': game.player.moves
    })