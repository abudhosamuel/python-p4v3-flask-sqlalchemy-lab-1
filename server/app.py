#!/usr/bin/env python3

import os
from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize migrations
migrate = Migrate(app, db)
db.init_app(app)

# Index route for the home page
@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

# View to get all earthquakes
@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    earthquakes = Earthquake.query.all()
    if earthquakes:
        earthquakes_list = [e.serialize() for e in earthquakes]
        return make_response(jsonify(earthquakes_list), 200)
    else:
        return make_response(jsonify({"message": "No earthquakes found."}), 404)

# View to get a specific earthquake by id
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)  # Simplified to use .get() instead of filter_by
    if earthquake:
        return make_response(jsonify(earthquake.serialize()), 200)
    else:
        return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)

# View to get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if earthquakes:
        quakes_list = [e.serialize() for e in earthquakes]
        response_body = {
            "count": len(quakes_list),
            "quakes": quakes_list
        }
        return make_response(jsonify(response_body), 200)
    else:
        return make_response(jsonify({"count": 0, "quakes": []}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
