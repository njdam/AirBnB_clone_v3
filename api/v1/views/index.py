#!/usr/bin/python3
"""THis is the index page view"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods='GET')
def status():
    """ A function to return status of API. """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods='GET')
def count():
    """ A function to return a number of each objects by type. """
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
