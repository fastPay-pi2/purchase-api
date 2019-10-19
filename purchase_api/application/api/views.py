from flask import Blueprint, request
from flask_restful import Resource, Api
from application.api.models import CartModel, PurchaseModel
from application.api.controller import validate_rfid, \
                                       http_request, \
                                       get_doc_by_attr, \
                                       save_cart, \
                                       update_cart, \
                                       save_purchase, \
                                       handle_exceptions, \
                                       delete_cart, \
                                       get_all_carts, \
                                       update_purchase, \
                                       post_purchase, \
                                       db_dump
from mongoengine.errors import DoesNotExist, NotUniqueError
import sys
import os   
from requests.exceptions import HTTPError
import json
from flask_cors import CORS
import sys


views_blueprint = Blueprint('views', __name__)
api = Api(views_blueprint)
CORS(views_blueprint)


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

    def put(self, rfid):
        post_data = request.get_json()
        new_rfid = post_data['rfid']
        success_message = {
            "message": f"Cart {rfid} successfully updated to {new_rfid}"
        }
        return handle_exceptions(update_cart, success_message,
                                 new_rfid, rfid)
        
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
        

api.add_resource(Cart, '/api/cart/<rfid>',
                 endpoint="cart",
                 methods=['GET', 'DELETE', 'PUT'])
# https://github.com/flask-restful/flask-restful/issues/114
api.add_resource(Cart, '/api/cart/',
                 endpoint="carts",
                 methods=['GET', 'POST'])
api.add_resource(Purchase, '/api/purchase/',
                 endpoint="purchase",
                 methods=['POST', 'GET'])
api.add_resource(Purchase, '/api/purchase/<purchase_id>',
                 endpoint="update_purchase",
                 methods=['PUT'])
api.add_resource(Purchase, '/api/purchase/',
                 endpoint="all_purchases",
                 methods=['GET'])
