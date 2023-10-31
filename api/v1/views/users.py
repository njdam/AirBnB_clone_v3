#!/usr/bin/python3
"""This is the users views"""

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """returns list of all users"""
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id=None):
    """Gets a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id=None):
    """Deletes a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a user"""
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    if "email" not in request.get_json():
        abort(400, 'Missing email')
    if "password" not in request.get_json():
        abort(400, 'Missing password')
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user_by_id(user_id=None):
    """Updates a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    return jsonify(user.to_dict())
