"""

This file has the website backend routes, form handling, and anything else for the
website's main architecture

"""
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from db_models import db
from routes import register_routes
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db.init_app(app)
####### Routes
@app.route("/Home")
@app.route("/")
def index():
    return render_template("index.html")

####### Run Program
with app.app_context():
    db.create_all()

# Register All Routes in the Program
register_routes(app)

if __name__ == '__main__':
    app.run()