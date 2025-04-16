from flask import render_template, request, redirect, url_for, jsonify
from db_models import db, Games, Game_Sounds, Programs, Groups, Members
import uuid

def register_games_routes(app):
    # View Games
    @app.route("/ViewGames")
    def ViewGames():
        sounds = Game_Sounds.query.all()
        games = Games.query.all()
        programs = Programs.query.all()
        return render_template("Games/ViewGames.html", sounds=sounds, games=games, programs=programs)
    
    # Add Game
    @app.route("/ViewGames/AddGames")
    def AddGames():
        my_uuid = uuid.uuid4()
        sounds = Game_Sounds.query.all()
        return render_template("Games/AddGames.html", uuid=my_uuid, sounds=sounds)

    # Add Game to Db
    @app.route("/ViewGames/AddGames/Add_Game", methods=['POST'])
    def add_game():
        game_id = request.form['Id']
        game_name = request.form['game_name']

        # Create a new game record
        new_game = Games(id=game_id, name=game_name)
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

    # Delete Game
    @app.route("/ViewGames/DeleteGame/<string:game_id>", methods=['POST'])
    def delete_game(game_id):
        game = Games.query.get(game_id)
        if game:
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for("ViewGames"))
        else:
            return "Error"
        