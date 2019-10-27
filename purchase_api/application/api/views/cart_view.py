from flask_restful import Resource, Api
from flask import Blueprint, request
from flask_cors import CORS

from application.api.controllers.cart_controller import (
    save_cart, update_cart, delete_cart, get_carts
)
from application.api.utils import (
    decorators
)

cart_blueprint = Blueprint('cart_view', __name__)
api = Api(cart_blueprint)
CORS(cart_blueprint)


class Cart(Resource):
    @decorators.handle_exceptions
    def get(self, rfid=None):
        carts, status = get_carts(rfid)
        return carts, status

    @decorators.handle_exceptions
    def post(self):
        post_data = request.get_json()
        if 'rfid' in post_data:
            rfid = post_data['rfid']
            response, status = save_cart(rfid)
            return response, status
        else:
            err = 'RFID is missing'
            return err, 400

    @decorators.handle_exceptions
    def put(self, rfid):
        post_data = request.get_json()
        if 'new_rfid' in post_data:
            new_rfid = post_data['new_rfid']
            response, status = update_cart(rfid, new_rfid)
            return response, status
        else:
            err = 'New RFID is missing'
            return err, 400

    @decorators.handle_exceptions
    def delete(self, rfid):
        response, status = delete_cart(rfid)
        return response, status


api.add_resource(Cart, '/api/cart/<rfid>',
                 endpoint="cart",
                 methods=['GET', 'DELETE', 'PUT'])
# https://github.com/flask-restful/flask-restful/issues/114
api.add_resource(Cart, '/api/cart/',
                 endpoint="carts",
                 methods=['GET', 'POST'])
