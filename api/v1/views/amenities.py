#!/usr/bin/python3
"""HolbertonBnB Amenity view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def amenities():
    """Defines the GET and POST method for amenities route.

    GET - Retries a list of all the Amenity objects.
    POST - Create a Amenity.
    """

    # GET method
    if request.method == "GET":
        return jsonify([s.to_dict() for s in storage.all("Amenity").values()])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "PUT", "DELETE"])
def amenity_id(amenity_id):
    """Defines the GET, PUT and DELETE methods for a spacific ID on amenities.

    GET - Retrieves a Amenity object with the given id.
    PUT - Updates a Amneity object with the given id using a json key/value
    DELETE = Deletes a Amenity object with the given id.
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify(amenity.to_dict())

    # DELETE method
    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    # PUT method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 404
    avoid = {"id", "created_at", "updated_at"}
    [setattr(amenity, k, v) for k, v in data.items() if k not in avoid]
    amenity.save()
    return jsonify(amenity.to_dict())