from flask import Blueprint, send_from_directory, current_app
import os

spacer_bp = Blueprint('spacer', __name__, url_prefix='/spacer')

# Base path to the web build folder
BUILD_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), 'build', 'web'))

@spacer_bp.route('/', defaults={'path': ''})
@spacer_bp.route('/<path:path>')
def serve_spa(path):
    file_path = os.path.join(BUILD_PATH, path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return send_from_directory(BUILD_PATH, path)
    else:
        # Fallback to index.html for client-side routing
        return send_from_directory(BUILD_PATH, 'index.html')

# @spacer_bp.route('/')
# def serve_index():
#     return send_from_directory(BUILD_PATH, 'index.html')

# @spacer_bp.route('/<path:filename>')
# def serve_static(filename):
#     return send_from_directory(BUILD_PATH, filename)
