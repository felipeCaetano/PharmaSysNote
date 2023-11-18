from enum import unique
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

from tablesdb import User

data_base = SQLAlchemy()


class AppConfiguration:
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///./db.sqlite"


app = Flask(__name__)
app.config.from_object(AppConfiguration)
data_base.init_app(app)

@app.route("/register", methods=["POST"])
def Register():
    user_data = request.get_json()
    user = User(email=user_data["email"], password=user_data['password'])
    data_base.session.add(user)
    data_base.session.commit()
    return True, 201

@app.route("/login", methods=["POST"])
def Login():
    email = request.json['email']
    password = request.json["password"]

with app.app_context():
    data_base.create_all()

if __name__ == "__main__":
    app.run(debug=True)