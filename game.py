from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('example.html')

@app.rout('/game')
def game():
  return render_template('title.html')

if __name__ == '__main__':
  app.run(debug = True)