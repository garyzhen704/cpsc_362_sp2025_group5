@app.route('/')
def index():
    return render_template('slot_display.html')