from flask import Flask, render_template
from blackjack.app import blackjack_bp  #Blackjack Blueprint

app = Flask(__name__)

app.register_blueprint(blackjack_bp, url_prefix='/blackjack') # Register the Blackjack Blueprint

@app.route('/')
def home():
    return render_template('homepage.html')  # Serve the homepage

@app.route('/brick-breaker')
def brick_breaker():
    return render_template('brick_breaker.html')  # Brick Breaker page


if __name__ == '__main__':
    app.run(debug=True)