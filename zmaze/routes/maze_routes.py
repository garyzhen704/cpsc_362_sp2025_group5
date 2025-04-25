from flask import Blueprint, render_template, request, jsonify, session
from zmaze.game_logic.maze_game import MazeGame

maze_bp = Blueprint('maze', __name__,
                    url_prefix='/maze',
                    template_folder='../templates',
                    static_folder='../static',
                    static_url_path='/static')

@maze_bp.route('/')
def maze_page():
    #render maze game page
    return render_template('maze.html')

@maze_bp.route('/maze')
def maze_game_page():
    #render maze game page (alternative route)
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

@maze_bp.route('/move', methods=['POST'])
def move():
    """Move the player in the specified direction"""
    if 'maze_game' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    data = request.get_json()
    direction = data.get('direction')
    
    if direction not in ['up', 'down', 'left', 'right']:
        return jsonify({'error': 'Invalid direction'}), 400
    
    # Recreate game from session
    game = MazeGame()
    game.maze = session['maze_game']['maze']
    player_pos = session['maze_game']['player_pos']
    game.player.reset(player_pos[0], player_pos[1])
    game.player.moves = session['maze_game']['moves']
    game.end_pos = session['maze_game']['end_pos']
    game.level = session['maze_game']['level']
    game.completed = session['maze_game']['completed']
    
    # Move player
    result = game.move_player(direction)
    
    # Update session
    session['maze_game'] = {
        'maze': game.maze,
        'player_pos': game.player.get_position(),
        'end_pos': game.end_pos,
        'level': game.level,
        'moves': game.player.moves,
        'completed': game.completed
    }
    
    return jsonify(result)

@maze_bp.route('/next-level', methods=['POST'])
def next_level():
    """Generate a new level"""
    if 'maze_game' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    # Recreate game from session
    game = MazeGame()
    game.maze = session['maze_game']['maze']
    player_pos = session['maze_game']['player_pos']
    game.player.reset(player_pos[0], player_pos[1])
    game.player.moves = session['maze_game']['moves']
    game.end_pos = session['maze_game']['end_pos']
    game.level = session['maze_game']['level']
    game.completed = session['maze_game']['completed']
    
    # Generate new level
    result = game.generate_new_level()
    
    # Update session
    session['maze_game'] = {
        'maze': game.maze,
        'player_pos': game.player.get_position(),
        'end_pos': game.end_pos,
        'level': game.level,
        'moves': game.player.moves,
        'completed': game.completed
    }
    
    return jsonify(result)