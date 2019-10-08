from flask import jsonify, Blueprint, request
from flask_cors import CORS
import re
import json
import sys
import requests
import os

views_blueprint = Blueprint("views", __name__)
CORS(views_blueprint)


@views_blueprint.route("/api/ping", methods=["GET"])
def ping():
    return jsonify(
        {
            "message": "success"
        }
    ), 200

@views_blueprint.route("/api/purchase", methods=["POST", "PUT", "DELETE"])
def purchase():
    if request.method == 'POST':
        post_json = json.loads(request.data)
        products_api = os.getenv("PRODUCTS_API", "")
        for item in post_json['items']:
            if re.search(r'^[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                      r'[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                      r'[0-9A-F]{2}$',
                      item):
                pass
                # requests para a api de produtos
                # products_api = os.getenv("PRODUCTS_API", "") + f"product/{item}"
                # requests.get(product)
            else:
                pass
                # deu ruim
        return jsonify(
            {
                "message": "POST success"
            }
        ), 200
    if request.method == 'DELETE':
        return jsonify(
            {
                "message": "DELETE success"
            }
        ), 200
    if request.method == 'PUT':
        return jsonify(
            {
                "message": "PUT success"
            }
        ), 200
