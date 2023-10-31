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

"""
@app_views.route('/status')
def get_status():
    '''This is the status of the api
    '''
    return jsonify(status='OK')


@app_views.route('/stats')
def get_stats():
    '''Gets the number of objects for each type.
    '''
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)


# For Task 3. Status of your API
@app_views.route('/status', methods=['GET'])
def status():
    '''This is the status of the api'''
    return jsonify({'status': 'OK'})


# For Task 4. Some stats?
@app_views.route('/stats', methods=['GET'])
def count():
    '''Getting number of each objects by type.'''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
"""

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    ''' routes to status page '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    '''retrieves the number of each objects by type'''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
