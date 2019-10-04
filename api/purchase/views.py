from flask import jsonify, Blueprint
from flask_cors import CORS

views_blueprint = Blueprint("views", __name__)
CORS(views_blueprint)


@views_blueprint.route("/api/ping", methods=["GET"])
def ping():
    return jsonify(
        {
            "message": "success"
        }
    ), 200
