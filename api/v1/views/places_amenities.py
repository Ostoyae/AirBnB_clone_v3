# /usr/bin/python3
"""Defines the view for places amenities Api calls"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort, jsonify, request
import os


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def show_place_amenities(place_id):
    """Defines the GET method for getting a list of amenities
    from a place on id

    GET - Retrives amenities from a place based on id
    """
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    return jsonify([a.to_dict() for a in place.amenities])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST", "DELETE"]
)
def manage_place_amenities(place_id, amenity_id):
    """Defines the POST and DELETE methods for a Amenity object
    for a Place object

    DELETE - remote an Amenity object from a place based on id
    POST - Addes an Amenity object from a place based on id
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    exists = False
    if place is None or amenity is None:
        abort(404)

    # POST
    if request.method == "POST":
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            # do the db stuff
            if amenity in place.amenities:
                exists = True
            place.amenities.append(amenity)
        else:
            if amenity.id in place.amenity_ids:
                exists = True
            place.amenity_ids.append(amenity.id)

        place.save()
        return jsonify(amenity.to_dict()), (200 if exists else 201)
        # return jsonify(amenity.to_dict()), 201

    # DELETE
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenities_ids:
            abort(404)
        place.amenities_ids.remove(amenity.id)
    place.save()
    return jsonify({}), 200
