import uuid
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
####### Database Table Model
db = SQLAlchemy()

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
    programs_id = db.Column(db.String(80), db.ForeignKey('programs.id'), nullable = True)
    groups = db.relationship('Groups', backref='game', cascade='all, delete', lazy=True)

# Program Lists
class Programs(db.Model):
        id = db.Column(db.String(80), primary_key = True)
        name = db.Column(db.String(80), nullable = False)
        state = db.Column(db.Boolean, default=False, nullable=False)
        games = db.relationship('Games', backref='programs', lazy = True, order_by = 'Games.name')

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