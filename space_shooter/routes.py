from flask import Blueprint, send_from_directory, current_app
import os

spacer_bp = Blueprint('spacer', __name__, url_prefix='/spacer')

# Base path to the web build folder
BUILD_PATH = os.path.join(os.path.dirname(__file__), 'build', 'web')

@spacer_bp.route('/')
def serve_index():
    return send_from_directory(BUILD_PATH, 'index.html')

@spacer_bp.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BUILD_PATH, filename)
