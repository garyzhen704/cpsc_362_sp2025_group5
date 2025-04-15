from flask import Flask, render_template
from blackjack.app import blackjack_bp  #Blackjack Blueprint
from flask_socketio import SocketIO
from blackjack.app import TitleNamespace, ScreenNamespace


app = Flask(__name__)

socketio = SocketIO(app)

app.register_blueprint(blackjack_bp, url_prefix='/blackjack') # Register the Blackjack Blueprint

socketio.on_namespace(TitleNamespace('/title')) # added
socketio.on_namespace(ScreenNamespace('/game_screen')) #added

@app.route('/')
def home():
    return render_template('home.html')  # Serve the homepage

@app.route('/brick-breaker')
def brick_breaker():
    return render_template('brick_breaker.html')  # Brick Breaker page


if __name__ == '__main__':
    socketio.run(app, debug=True)
    app.run(debug=True)