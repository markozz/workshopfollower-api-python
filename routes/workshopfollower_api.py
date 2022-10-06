"""Workshopfollower API Endpoints"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint

from validate_email import validate_email
WORKSHOPFOLLOWER_API = Blueprint('workshopfollower_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return WORKSHOPFOLLOWER_API


WORKSHOPFOLLOWERS_STORAGE = {
    "8c36e86c-13b9-4102-a44f-646015dfd981": {
        'name': u'Marcus Lenaiobi',
        'email': u'testuser1@test.com',
        'createdAt': (datetime.today() - timedelta(1)).isoformat()
    },
    "04cfc704-acb2-40af-a8d3-4611fab54ada": {
        'name': u'Jerom Sterkie',
        'email': u'testuser2@test.com',
        'createdAt': (datetime.today() - timedelta(2)).isoformat()
    }
}


@WORKSHOPFOLLOWER_API.route('/workshopfollowers', methods=['GET'])
def get_records():
    """Return all workshopfollowers
    @return: 200: an array of all known WORKSHOPFOLLOWERS_STORAGE as a \
    flask/response object with application/json mimetype.
    """
    workshopfollowers = []
    for id in WORKSHOPFOLLOWERS_STORAGE:
        workshopfollowers.append({
            "id" : id,
            "name" : WORKSHOPFOLLOWERS_STORAGE[id]['name'],
            "email" : WORKSHOPFOLLOWERS_STORAGE[id]['email'],
            "createdAt": WORKSHOPFOLLOWERS_STORAGE[id]['createdAt']
        })
    return jsonify({'workshopfollowers': workshopfollowers})


@WORKSHOPFOLLOWER_API.route('/workshopfollowers/<string:_id>', methods=['GET'])
def get_record_by_id(_id):
    """Get workshopfollower details by it's id
    @param _id: the id
    @return: 200: a workshopfollower as a flask/response object \
    with application/json mimetype.
    @raise 404: if workshopfollower not found
    """
    if _id not in WORKSHOPFOLLOWERS_STORAGE:
        abort(404)
    return jsonify(WORKSHOPFOLLOWERS_STORAGE[_id])


@WORKSHOPFOLLOWER_API.route('/workshopfollowers', methods=['POST'])
def create_record():
    """Create a workshopfollower record
    @param email: post : the email address of the workshopfollower
    @param name: post : the name of the workshopfollower
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('name'):
        abort(400)

    new_uuid = str(uuid.uuid4())
    workshopfollower = {
        'name': data['name'],
        'email': data['email'],
        'createdAt': datetime.now().isoformat()
    }
    WORKSHOPFOLLOWERS_STORAGE[new_uuid] = workshopfollower
    # HTTP 201 Created
    return jsonify({"id": new_uuid}), 201


@WORKSHOPFOLLOWER_API.route('/workshopfollowers/<string:_id>', methods=['PUT'])
def edit_record(_id):
    """Edit a workshopfollower record
    @param email: post : the email address of the workshopfollower
    @param name: post : the name of the workshopfollower
    @return: 200: a workshopfollower as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if _id not in WORKSHOPFOLLOWERS_STORAGE:
        abort(404)

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('name'):
        abort(400)

    workshopfollower = {
        'name': data['name'],
        'email': data['email'],
        'createdAt': datetime.now().isoformat()
    }

    WORKSHOPFOLLOWERS_STORAGE[_id] = workshopfollower
    return jsonify(WORKSHOPFOLLOWERS_STORAGE[_id]), 200


@WORKSHOPFOLLOWER_API.route('/workshopfollowers/<string:_id>', methods=['DELETE'])
def delete_record(_id):
    """Delete a workshopfollower record
    @param id: the id
    @return: 204: an empty payload.
    @raise 404: if book request not found
    """
    if _id not in WORKSHOPFOLLOWERS_STORAGE:
        abort(404)

    del WORKSHOPFOLLOWERS_STORAGE[_id]

    return jsonify({'message': 'deleted'}), 204

# @WORKSHOPFOLLOWER_API.route('/bullshit', methods=['GET'])
# def bullshit():
#     return jsonify({'name': 'Bull Shit', 'birthday': '14-09-1988'})
