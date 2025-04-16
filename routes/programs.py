from flask import render_template, request, redirect, url_for, jsonify
from db_models import db, Programs, Games
import uuid

def register_programs_routes(app):
    # Create a Program
    @app.route("/ViewGames/CreateProgram", methods=['GET', 'POST'])
    def CreateProgram():
        if request.method == 'POST':
            program_name = request.form['name']
            game_state = request.form['program_state']

            if game_state.lower() == "true":
                game_state = True
            else:
                game_state = False

            selected_game_ids = request.form.getlist('games')  # This will be a list of game IDs

            new_program = Programs(id=str(uuid.uuid4()), name=program_name, state=game_state)
            db.session.add(new_program)

            for game_id in selected_game_ids:
                game = Games.query.get(game_id)
                if game:
                    game.programs_id = new_program.id  # Assign the program

            db.session.commit()
            return redirect(url_for('ViewGames'))

        games = Games.query.all()
        return render_template("Events/CreateProgram.html", games=games)

    # Change a Program State
    @app.route("/ViewGames/ChangeState/<string:program_id>", methods=['POST'])
    def change_state(program_id):
        program = Programs.query.get(program_id)
        
        if program:
            # Ensure the state is either 0 (False) or 1 (True) and toggle it
            if program.state == 0:
                program.state = 1  # Set to True
            elif program.state == 1:
                program.state = 0  # Set to False
            else:
                # If the state is neither 0 nor 1, set it to 0 (default False)
                program.state = 0
            
            db.session.commit()
            return redirect(url_for("ViewGames"))
        else:
            return jsonify({"error": "Game not found"}), 404
    
    # Delete a program
    @app.route("/ViewGames/DeleteProgram/<string:program_id>", methods=['POST'])
    def delete_program(program_id):
        program = Programs.query.get(program_id)
        if program:
            db.session.delete(program)
            db.session.commit()
            return redirect(url_for("ViewGames"))
        else:
            return "Error"