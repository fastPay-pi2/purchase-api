from flask_restful import Resource, Api
from flask import Blueprint, request
from flask_cors import CORS

from application.api.utils import (
    validators,
    data_formatter,
    handlers
)
from application.api.controllers.purchase_controller import (
    server_update_purchase, start_purchase, get_purchases, delete_purchase
)

purchase_blueprint = Blueprint('views', __name__)
api = Api(purchase_blueprint)
CORS(purchase_blueprint)


class Purchase(Resource):
    def post(self):
        data = request.get_json()
        err = validators.validate_fields(data, 'user_id', 'cart_id')
        if err:
            err = f'Fields are missing: {", ".join(err)}'
            return data_formatter.format_message(err, 400)
        else:
            return start_purchase(data)

    def put(self, user_id=None):
        data = request.get_json()
        err = validators.validate_fields(data, 'state', 'user_id')
        if err:
            err = f'Fields are missing: {", ".join(err)}'
            return data_formatter.format_message(err, 400)
        else:
            success_message = f"Purchase successfully updated"
            return handlers.handle_exceptions(server_update_purchase,
                                              success_message,
                                              data)

    def get(self, user_id=None):
        purchases = get_purchases(user_id)
        return purchases, 200

    def delete(self, purchase_id):
        success_message = f'Purchase {purchase_id} successfully removed'

        return handlers.handle_exceptions(delete_purchase, success_message,
                                          str(purchase_id))


api.add_resource(Purchase, '/api/purchase/',
                 endpoint="purchase",
                 methods=['POST', 'GET'])
api.add_resource(Purchase, '/api/purchase/',
                 endpoint="server_update_purchase",
                 methods=['PUT'])
api.add_resource(Purchase, '/api/purchase/<user_id>',
                 endpoint="user_update_purchase",
                 methods=['PUT', 'DELETE'])
api.add_resource(Purchase, '/api/userpurchases/<user_id>',
                 endpoint="list_user_purchases",
                 methods=['GET'])
