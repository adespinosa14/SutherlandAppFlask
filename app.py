from flask import Flask, render_template

app = Flask(__name__)

@app.route("/Home")
@app.route("/")
def index():
    return render_template("index.html")

# Event Routes
@app.route("/CurrentEvents")
def CurrentEvents():
    return render_template("Events/ViewEvents.html")

@app.route("/ViewEvents/AddEvent")
def AddEvent():
    return render_template("Events/AddEvent.html")

# Game Routes
@app.route("/ViewGames")
def ViewGames():
    return render_template("Games/ViewGames.html")

@app.route("/ViewGames/AddGames")
def AddGames():
    return render_template("Games/AddGames.html")

@app.route("/ViewGames/AddSounds")
def AddSounds():
    return render_template("Games/AddSounds.html")

# Run Program
if __name__ == '__main__':
    app.run()