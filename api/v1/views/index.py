#!/usr/bin/python3
"""THis is the index page view"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# For Task 3. Status of your API
@app_views.route('/status', methods=['GET'])
def get_status():
    """This is the status of the api"""
    return jsonify({'status': 'OK'})


# For Task 4. Some stats?
@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Gets the stats of all objects"""
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    objects_count = {}
    for key in objects:
        objects_count[key] = storage.count(objects[key])
    return jsonify(objects_count)
