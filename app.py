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
        return f'<User {self.Event_Name}>'
# Game Sounds
class Game_Sounds(db.Model):
    __tablename__ = 'game__sounds'
    id = db.Column(db.String(80), primary_key = True)
    Sound_Name = db.Column(db.String(80), nullable = False)
    File = db.Column(db.LargeBinary, nullable = False)
    
    def __repr__(self):
        return f'<Sound {self.Sound_Name}>'

# Game Components
class Games(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    groups = db.relationship('Groups', backref='game', lazy=True)

# Groups Table
class Groups(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    game_id = db.Column(db.String(80), db.ForeignKey('games.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    members = db.relationship('Members', backref='group', lazy=True)

# Members Table
class Members(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    group_id = db.Column(db.String(80), db.ForeignKey('groups.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    sounds = db.relationship('MemberSounds', backref='member', lazy=True)

# Member Sound
class MemberSounds(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    member_id = db.Column(db.String(36), db.ForeignKey('members.id'), nullable=False)
    sound_id = db.Column(db.String(80), db.ForeignKey('game__sounds.id'), nullable=False)

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
    sounds = Game_Sounds.query.all()
    return render_template("Games/ViewGames.html", sounds=sounds)

#########################################################################      ADD GAMES START
@app.route("/ViewGames/AddGames")
def AddGames():
    my_uuid = uuid.uuid4()
    sounds = Game_Sounds.query.all()



    return render_template("Games/AddGames.html", uuid=my_uuid, sounds=sounds)

#########################################################################      ADD GAMES END
@app.route("/ViewGames/AddSounds")
def AddSounds():
    my_uuid = uuid.uuid4()
    return render_template("Games/AddSounds.html", uuid=my_uuid)

@app.route("/ViewGames/AddSounds/add_sound", methods=['POST'])
def add_sound():
    if request.method == 'POST':
        Id = request.form['Id']
        sound_name = request.form['Sound_Name']
        file = request.files['File']
        print(f"Id: {Id}\nSound Name: {sound_name}\nFile: {file.filename}")

        new_sound = Game_Sounds(
            id = Id,
            Sound_Name = sound_name,
            File = file.read())
        db.session.add(new_sound)
        db.session.commit()

        return redirect(url_for('ViewGames'))

@app.route("/ViewGames/Delete_Sound/<string:sound_id>", methods=['POST'])
def Delete_Sound(sound_id):
    id = Game_Sounds.query.get(sound_id)
    print(id)
    if id:
        db.session.delete(id)
        db.session.commit()
        return redirect(url_for('ViewGames'))
    return "Sound Not Found"

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