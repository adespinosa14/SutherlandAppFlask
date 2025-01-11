"""

This file has the website backend routes, form handling, and anything else for the
website's main architecture

"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQL_TRACK_MODIFICATION'] = False

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

#Database Table Model
db = SQLAlchemy(app)
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Event_Name = db.Column(db.String(80), nullable = False)
    Event_Description = db.Column(db.String(120), nullable = False)
    Event_Location  = db.Column(db.String(120), nullable = False)
    Event_Date = db.Column(db.Date(), nullable = False)

    def __repr__(self):
        return f'<User {self.username}>'

# Run Program
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()