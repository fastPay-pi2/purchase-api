from flask import Blueprint, request
from flask_restful import Resource, Api
from application.api.controller import db_dump

from application.api.controllers.purchase_controller import save_purchase, update_purchase, post_purchase

from application.api.utils import validate_rfid, http_request, handle_exceptions

from flask_cors import CORS


purchase_blueprint = Blueprint('views', __name__)
api = Api(purchase_blueprint)
CORS(purchase_blueprint)


class Purchase(Resource):
    def post(self):
        post_data = request.get_json()
        return post_purchase(post_data)

    def put(self, purchase_id):
        post_data = request.get_json()
        success_message = {
            "message": f"Purchase {purchase_id} successfully updated"
        }
        return handle_exceptions(update_purchase,
                                 success_message,
                                 post_data, purchase_id)

    def get(self):
        db_json = db_dump()
        return db_json, 200
        

api.add_resource(Purchase, '/api/purchase/',
                 endpoint="purchase",
                 methods=['POST', 'GET'])
api.add_resource(Purchase, '/api/purchase/<purchase_id>',
                 endpoint="update_purchase",
                 methods=['PUT'])
api.add_resource(Purchase, '/api/purchase/',
                 endpoint="all_purchases",
                 methods=['GET'])
