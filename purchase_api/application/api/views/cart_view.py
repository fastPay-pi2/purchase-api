from flask import Blueprint, request
from flask_restful import Resource, Api
from application.api.controllers.cart_controller import save_cart, update_cart, delete_cart, get_all_carts
from application.api.models.cart_model import CartModel


from application.api.controller import get_doc_by_attr, \
                                       db_dump


from application.api.utils import validate_rfid, http_request, handle_exceptions

from flask_cors import CORS

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
            return handle_exceptions(get_doc_by_attr, success_message,
                                     CartModel,"rfid", rfid)
    
    def post(self):
        post_data = request.get_json()
        cart_rfid = post_data['rfid']
        success_message = {
                'message': f'Cart {cart_rfid} successfully added'
        }
        return handle_exceptions(save_cart,
                                 success_message, cart_rfid)

    def delete(self, rfid):
        success_message = {
                'message': f'Cart {rfid} successfully removed'
        }
        return handle_exceptions(delete_cart,
                                 success_message, rfid)


api.add_resource(Cart, '/api/cart/<rfid>',
                 endpoint="cart",
                 methods=['GET', 'DELETE', 'PUT'])
# https://github.com/flask-restful/flask-restful/issues/114
api.add_resource(Cart, '/api/cart/',
                 endpoint="carts",
                 methods=['GET', 'POST'])