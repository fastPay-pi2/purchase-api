from application.api.models import CartModel
from flask_restful import Resource, Api
from flask import Blueprint, request
from flask_cors import CORS

from application.api.controllers.cart_controller import (
    save_cart, update_cart, delete_cart, get_all_carts
)
from application.api.utils import (
    db_utils,
    handlers
)

cart_blueprint = Blueprint('cart_view', __name__)
api = Api(cart_blueprint)
CORS(cart_blueprint)


class Cart(Resource):
    def get(self, rfid=None):
        if rfid is None:
            return get_all_carts(rfid)
        else:
            success_message = {
                'cart': rfid
            }
            return handlers.handle_exceptions(
                db_utils.get_doc_by_attr, success_message,
                CartModel, "rfid", rfid
            )

    def post(self):
        post_data = request.get_json()
        if 'rfid' in post_data:
            cart_rfid = post_data['rfid']
            success_message = f'Cart {cart_rfid} successfully added'

            return handlers.handle_exceptions(save_cart, success_message,
                                              cart_rfid)
        else:
            return {'error': 'RFID is missing'}, 400

    def put(self, rfid):
        post_data = request.get_json()
        if 'new_rfid' in post_data:
            new_rfid = post_data['new_rfid']
            success_message = f'Cart {new_rfid} successfully updated'

            return handlers.handle_exceptions(update_cart, success_message,
                                              str(new_rfid), str(rfid))
        else:
            return {'error': 'NEW RFID is missing'}, 400

    def delete(self, rfid):
        success_message = f'Cart {rfid} successfully removed'

        return handlers.handle_exceptions(delete_cart, success_message,
                                          str(rfid))


api.add_resource(Cart, '/api/cart/<rfid>',
                 endpoint="cart",
                 methods=['GET', 'DELETE', 'PUT'])
# https://github.com/flask-restful/flask-restful/issues/114
api.add_resource(Cart, '/api/cart/',
                 endpoint="carts",
                 methods=['GET', 'POST'])
