#!/usr/bin/python3
"""A host file for new view for Review object that handles
all default RESTFul API actions
"""

# Importing modules from system files
from flask import request, jsonify, abort

# Importing modules from project files
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage, storage_t


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_of_place(place_id=None):
    """A function to retrieve a list of all Review objects of a Place."""
    all_places = storage.all("Place").values()

    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)

    reviews = [obj.to_dict() for obj in storage.all("Review").values()
                    if place_id == obj.place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id=None):
    """A function to retrieve list of all Review object."""
    all_reviews = storage.all("Review").values()
    obj = [obj.to_dict() for obj in all_reviews if obj.id == review_id]
    if obj == []:
        abort(404)
    return jsonify(obj[0])


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def remove_review(review_id=None):
    """A function to delete review object."""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_review(place_id=None):
    """A function to add review object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if type(data) is not dict:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')

    # If place id is available and linked to place save it's review
    data[place_id] = place_id
    new_review = Review(**data)
    new_review.save()
    # Return the new review with status code 201
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id=None):
    """A function to update review object."""
    ignored_keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')

    if review_id:
        review = storage.get(Review, review_id)
        if review:
            data = request.get_json()
            if type(data) is not dict:
                abort(400, 'Not a JSON')
            for key, value in data.items():
                if key not in ignored_keys:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
    else:
        abort(404)
