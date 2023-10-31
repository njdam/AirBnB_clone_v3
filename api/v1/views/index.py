#!/usr/bin/python3
"""THis is the index page view"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ A function to return status of API. """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def count():
    """ A function to return a number of each objects by type. """
    total = {}
    classes = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for cls in classes:
        count = storage.count(cls)
        total[classes.get(cls)] = count
    return jsonify(total)
