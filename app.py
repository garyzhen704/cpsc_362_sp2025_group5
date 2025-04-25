from flask import Flask, render_template, redirect, url_for
from blackjack.app import blackjack_bp  #Blackjack Blueprint
from flask_socketio import SocketIO
from blackjack.app import TitleNamespace, ScreenNamespace
from zmaze.routes.maze_routes import maze_bp  # Import Zmaze Blueprint
from Slot_Machine.app import slot_bp
import os  # For debugging


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for zmaze session management

# Debug - print template folders
print("Main app template folder:", os.path.abspath(app.template_folder))
zmaze_template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zmaze', 'templates')
print("ZMaze template folder:", zmaze_template_folder)

socketio = SocketIO(app)

app.register_blueprint(blackjack_bp, url_prefix='/blackjack') # Register the Blackjack Blueprint
app.register_blueprint(maze_bp, url_prefix='/zmaze') # Register the Zmaze Blueprint
app.register_blueprint(slot_bp, url_prefix='/slotmachine')

socketio.on_namespace(TitleNamespace('/title')) # added
socketio.on_namespace(ScreenNamespace('/game_screen')) #added

@app.route('/')
def home():
    return render_template('home.html')  # Serve the homepage

@app.route('/brick-breaker')
def brick_breaker():
    return render_template('brick_breaker.html')  # Brick Breaker page

@app.route('/zmaze')
def zmaze():
    return redirect(url_for('maze.maze_page'))  # Redirect to the Zmaze blueprint route

if __name__ == '__main__':
    socketio.run(app, debug=True)