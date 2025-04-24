import sys
import os

# Add the parent directory to sys.path to allow importing from modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__, 
                static_folder="static",
                template_folder="templates")
    app.secret_key = 'your_secret_key_here'  # Required for session management
    
    # Import blueprint after Flask app is created to avoid circular imports
    from routes.maze_routes import maze_bp
    
    # Register the maze blueprint
    app.register_blueprint(maze_bp)
    
    @app.route('/')
    def index():
        return redirect(url_for('maze.maze_page'))
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)