from flask import render_template, request, redirect, url_for, jsonify
from db_models import db, Events, Programs
import uuid

def register_event_routes(app):

    # View Current Events
    @app.route("/CurrentEvents")
    def CurrentEvents():
        events = Events.query.all()
        programs = Programs.query.all()
        print(programs)
        return render_template("Events/ViewEvents.html", events=events, programs=programs)
    
    # Add Events
    @app.route("/ViewEvents/AddEvent")
    def AddEvent():
        my_uuid = uuid.uuid4()
        return render_template("Events/AddEvent.html", uuid=my_uuid)
    
    # Add Event to Database
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
    
    # Delete Event
    @app.route("/ViewEvents/DeleteEvent/<string:event_id>", methods=['POST'])
    def delete_event(event_id):
        event = Events.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return redirect(url_for('CurrentEvents'))
        return "Event not found", 404
