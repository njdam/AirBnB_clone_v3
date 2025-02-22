#!/usr/bin/python3
"""A host file for a new view for Place objects that handles
all default RESTFul API actions
"""

# Importing modules from system files
from flask import request, jsonify, abort

# Importing modules from project files
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_of_city(city_id=None):
    """A function to list all Places' objects in city"""
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    list_places = [obj.to_dict() for obj in storage.all("Place").values()
                   if city_id == obj.city_id]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id=None):
    """A function to retrieve list of all place objects of a city."""
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    return jsonify(place_obj[0])


@app_views.route('/places/<place_id>', methods=['DELETE'])
def remove_place(place_id=None):
    """A function to delete the place object."""
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            storage.delete(place)
            storage.save()
            return (jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id=None):
    """A function to add a place object."""
    city = storage.get(City, city_id)
    if not city:
        raise abort(404)
    data = request.get_json()
    if type(data) is not dict:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')

    # If city id is available and linked to city save it in place
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    # Returning new place with status code 201
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id=None):
    """A function that update the place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    ignored_keys = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    data = request.get_json()
    if type(data) is not dict:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200
