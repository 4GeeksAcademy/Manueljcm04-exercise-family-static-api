"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
carrasco_family = FamilyStructure("Carrasco")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/members/carrasco', methods=['GET'])
def handle_hello_carrasco():

    # this is how you can use the Family datastructure by calling its methods
    members = carrasco_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/members/<int:id_member>', methods=['GET'])
def handle_get_member(id_member):
    member = jackson_family.get_member(id_member)

    if member is None:
        return jsonify({ 'err': 'member not found'}), 404

    response = member
    
    return jsonify(response), 200

@app.route('/members/<int:id_member>', methods=['DELETE'])
def handle_delete_member(id_member):
    member = jackson_family.get_member(id_member)

    if member is None:
        return jsonify({ 'err': 'member not found'}), 404

    jackson_family.delete_member(id_member)
    return jsonify({'message': 'Member deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/members', methods=['POST'])
def handle_add_member():
    data = request.json
    jackson_family.add_member(data)
    response_body = {}
    
    members = jackson_family.get_all_members()
    response_body["message"] = "Add it!"
    response_body["results"] = members
    return response_body, 200

if __name__ == '__main__':
    app.run(debug=True)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)