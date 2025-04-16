from flask import render_template, request, redirect, url_for, jsonify
import uuid
from db_models import db, Game_Sounds

def register_sound_routes(app):

    # Add Sound Page
    @app.route("/ViewGames/AddSounds")
    def AddSounds():
        my_uuid = uuid.uuid4()
        return render_template("Games/AddSounds.html", uuid=my_uuid)
    
    # Add Sound to Db
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
        
    # Delete Sound
    @app.route("/ViewGames/Delete_Sound/<string:sound_id>", methods=['POST'])
    def Delete_Sound(sound_id):
        id = Game_Sounds.query.get(sound_id)
        print(id)
        if id:
            db.session.delete(id)
            db.session.commit()
            return redirect(url_for('ViewGames'))
        return "Sound Not Found"