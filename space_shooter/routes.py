from flask import Blueprint, send_from_directory, current_app
import os

# Keeps your /spacer prefix
spacer_bp = Blueprint('spacer', __name__, url_prefix='/spacer')

@spacer_bp.route('/')
def serve_index():
    # This serves the main game HTML from the new static location
    game_dir = os.path.join(current_app.root_path, 'static', 'space_game')
    return send_from_directory(game_dir, 'index.html')

@spacer_bp.route('/<path:path>')
def serve_assets(path):
    # This serves the .apk, .js, .data and all assets to other computers
    game_dir = os.path.join(current_app.root_path, 'static', 'space_game')
    return send_from_directory(game_dir, path)
