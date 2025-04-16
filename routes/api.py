from io import BytesIO
import mimetypes
from flask import Response, render_template, redirect, url_for, jsonify
from db_models import Events, Programs, Games, Groups, Members, Game_Sounds

def register_api_routes(app):

    # Programs API
    @app.route('/api/programs', methods=['GET'])
    def api_get_programs():
        programs = Programs.query.all()
        output = []

        for program in programs:
            program_data = {
                'id': program.id,
                'name': program.name,
                'state': program.state,
                'games': [
                    {
                        'id': game.id,
                        'name': game.name,
                    } for game in program.games
                ]
            }
            output.append(program_data)

        return jsonify(output)
    
    # Get Specific Game API
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
            },
            "groups": groups_data
        }

        return jsonify(response_data), 200  # 200 OK
    
    # Total Game API
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
    
    # Get Events API
    @app.route("/api/events")
    def retrieve_events():
        events = Events.query.all()
        event_list = [event_to_dict(event) for event in events]
        return  jsonify(event_list)
    
    # Get all sounds API
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
    
        
    # Turn Events to a Dictionary
    def event_to_dict(event):
        return {
            "id": event.id,
            "Event_Name": event.Event_Name,
            "Event_Description": event.Event_Description,
            "Event_Location": event.Event_Location,
            "Event_Date": event.Event_Date.strftime("%Y-%m-%d")
        }