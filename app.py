"""

This file has the website backend routes, form handling, and anything else for the
website's main architecture

"""
import uuid
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Taffy2002!!!@localhost:3306/Event_Sound_Data'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

####### Database Table Model
db = SQLAlchemy(app)

# Event
class Events(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    Event_Name = db.Column(db.String(80), nullable = False)
    Event_Description = db.Column(db.String(120), nullable = False)
    Event_Location  = db.Column(db.String(120), nullable = False)
    Event_Date = db.Column(db.Date(), nullable = False)

    def __repr__(self):
        return f'<User {self.username}>'
# Game Sounds
class Game_Sounds(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    Sound = db.Column(db.File)

####### Routes
@app.route("/Home")
@app.route("/")
def index():
    return render_template("index.html")

####### Event Routes
@app.route("/CurrentEvents")
def CurrentEvents():
    events = Events.query.all()
    return render_template("Events/ViewEvents.html", events=events)

@app.route("/ViewEvents/AddEvent")
def AddEvent():
    my_uuid = uuid.uuid4()
    return render_template("Events/AddEvent.html", uuid=my_uuid)

####### Add Event
@app.route("/ViewEvents/AddEvent/add-event", methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
            eventID = request.form["eventID"]
            eventName = request.form['eventName']
            eventDescription = request.form['eventDescription']
            eventLocation = request.form['eventLocation']
            eventDate = request.form['eventDate']

            print(f"Event ID: {eventID}\nEvent Name: {eventName}\nEvent Description: {eventDescription}\nEvent Location: {eventLocation}\nEvent Date: {eventDate}")

            new_event = Events(id = eventID, 
                               Event_Name = eventName, 
                               Event_Description = eventDescription, 
                               Event_Location = eventLocation,
                               Event_Date = eventDate)

            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('CurrentEvents'))

    return redirect(url_for('AddEvent'))
####### Delete Event
@app.route("/ViewEvents/DeleteEvent/<string:event_id>", methods=['POST'])
def delete_event(event_id):
    event = Events.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('CurrentEvents'))
    return "Event not found", 404

####### Game Routes
@app.route("/ViewGames")
def ViewGames():
    return render_template("Games/ViewGames.html")

@app.route("/ViewGames/AddGames")
def AddGames():
    return render_template("Games/AddGames.html")

@app.route("/ViewGames/AddSounds")
def AddSounds():
    myuuid = uuid.uuid4()
    return render_template("Games/AddSounds.html", uuid=myuuid)

@app.route("/ViewGames/AddSounds/add_sound", methods=['POST'])
def add_sound():
    if request.method == 'POST':
        id = request.form['Id']
        sound = request.form['Sound']
        print(f"Id: {id}\nSound: {sound}")
        return redirect(url_for('AddGames'))

####### API calls to retrieve Event + Sound Data
@app.route("/api/events")
def retrieve_events():
    events = Events.query.all()
    event_list = [event_to_dict(event) for event in events]
    return  jsonify(event_list)

####### Convert Events to a Dictionary
def event_to_dict(event):
    return {
        "id": event.id,
        "Event_Name": event.Event_Name,
        "Event_Description": event.Event_Description,
        "Event_Location": event.Event_Location,
        "Event_Date": event.Event_Date.strftime("%Y-%m-%d")
    }

####### Run Program
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()