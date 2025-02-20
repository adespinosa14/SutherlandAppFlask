"""

This file has the website backend routes, form handling, and anything else for the
website's main architecture

"""
from io import BytesIO
import mimetypes
import uuid
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
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
    state = db.Column(db.Boolean, default=False, nullable=False)
    groups = db.relationship('Groups', backref='game', cascade='all, delete', lazy=True)

# Groups Table
class Groups(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    game_id = db.Column(db.String(80), db.ForeignKey('games.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    members = db.relationship('Members', backref='group', cascade='all, delete', lazy=True)

class Members(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.String(80), primary_key=True, default=str(uuid.uuid4()))
    group_id = db.Column(db.String(80), db.ForeignKey('groups.id'))
    name = db.Column(db.String(80))
    sound_id = db.Column(db.String(80))  # Store a single sound ID for each member


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
    games = Games.query.all()
    return render_template("Games/ViewGames.html", sounds=sounds, games=games)

@app.route("/ViewGames/DeleteGame/<string:game_id>", methods=['POST'])
def delete_game(game_id):
    game = Games.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
        return redirect(url_for("ViewGames"))
    else:
        return "Error"

@app.route("/ViewGames/ChangeState/<string:game_id>", methods=['POST'])
def change_state(game_id):
    game = Games.query.get(game_id)
    
    if game:
        # Ensure the state is either 0 (False) or 1 (True) and toggle it
        if game.state == 0:
            game.state = 1  # Set to True
        elif game.state == 1:
            game.state = 0  # Set to False
        else:
            # If the state is neither 0 nor 1, set it to 0 (default False)
            game.state = 0
        
        db.session.commit()
        return redirect(url_for("ViewGames"))
    else:
        return jsonify({"error": "Game not found"}), 404


#########################################################################      ADD GAMES START
@app.route("/ViewGames/AddGames")
def AddGames():
    my_uuid = uuid.uuid4()
    sounds = Game_Sounds.query.all()
    return render_template("Games/AddGames.html", uuid=my_uuid, sounds=sounds)

@app.route("/ViewGames/AddGames/Add_Game", methods=['POST'])
def add_game():
    game_id = request.form['Id']
    game_name = request.form['game_name']
    game_state = request.form['game_state']
    # Convert to boolean
    if game_state.lower() == "true":
        game_state = True
    else:
        game_state = False

    # Create a new game record
    new_game = Games(id=game_id, name=game_name, state=game_state)
    db.session.add(new_game)

    # Process groups and members
    group_ids = request.form.getlist('group_id[]')
    group_names = request.form.getlist('group_name[]')

    for i, group_id in enumerate(group_ids):
        group_name = group_names[i]
        new_group = Groups(id=group_id, game_id=game_id, name=group_name)
        db.session.add(new_group)

        member_names = request.form.getlist(f'member_name[{i + 1}][]')
        sound_ids = request.form.getlist(f'sound_id[{i + 1}][]')

        for j, member_name in enumerate(member_names):
            # Create a new member with a single sound
            sound_id = sound_ids[j]  # Each member picks one sound
            new_member = Members(
                id=str(uuid.uuid4()),
                group_id=group_id,
                name=member_name,
                sound_id=sound_id  # Associate the single sound with the member
            )
            db.session.add(new_member)

    db.session.commit()
    return redirect(url_for('ViewGames'))

# Create API Call
@app.route("/api/games/<game_id>", methods=['GET'])
def get_game(game_id):
    # Retrieve the game from the database
    game = Games.query.get(game_id)

    if not game:
        return jsonify({"error": "Game not found"}), 404  # 404 Not Found if the game doesn't exist

    # Retrieve the groups associated with the game
    groups = Groups.query.filter_by(game_id=game_id).all()

    groups_data = []
    for group in groups:
        # Retrieve members for each group
        members = Members.query.filter_by(group_id=group.id).all()
        members_data = []

        for member in members:
            members_data.append({
                "id": member.id,
                "name": member.name,
                "sound_id": member.sound_id
            })

        groups_data.append({
            "group_id": group.id,
            "group_name": group.name,
            "members": members_data
        })

    # Prepare the response data
    response_data = {
        "game": {
            "id": game.id,
            "name": game.name,
            "state": game.state
        },
        "groups": groups_data
    }

    return jsonify(response_data), 200  # 200 OK

# Create API Route
@app.route("/api/games", methods=["GET"])
def get_games():
    games = Games.query.all()
    response = []
    for game in games:
        game_data = {
            "id": game.id,
            "name": game.name,
            "state": game.state,
            "groups": []
        }
        response.append(game_data)
        for group in game.groups:
            group_data = {
                "id": group.id,
                "name": group.name,
                "members": [{"id": member.id, "name": member.name, "sound_id": member.sound_id} for member in group.members]
            }
            game_data["groups"].append(group_data)
    return jsonify(response)

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

@app.route('/api/sounds/<sound_id>', methods=['GET'])
def get_sound(sound_id):
    # Fetch the sound from the database
    sound = Game_Sounds.query.filter_by(id=sound_id).first()
    if not sound:
        return jsonify({"error": "Sound not found"}), 404

    # Assuming sound.audio contains the BLOB data of the audio file
    audio_data = sound.File
    mime_type, _ = mimetypes.guess_type(sound.Sound_Name)  # Assumes you store the file name
    if mime_type is None:
        mime_type = "audio/mpeg"  # Default to audio/mpeg if type could not be guessed
    
    return Response(BytesIO(audio_data), mimetype=mime_type)

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
