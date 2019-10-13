from flask import Blueprint, request
from flask_restful import Resource, Api
from application.api.models import CartModel, PurchaseModel
from application.api.controller import validate_rfid, http_request
from mongoengine.errors import DoesNotExist   
import sys
import os   
from requests.exceptions import HTTPError
import json
from flask_cors import CORS


views_blueprint = Blueprint('views', __name__)
api = Api(views_blueprint)
CORS(views_blueprint)


PRODUCTS_API = os.getenv("PRODUCTS_API", "")


class Cart(Resource):
    def get(self, rfid=None):
        if rfid is None:
            carts = []
            if not CartModel.objects:
                return carts, 200
            else:
                for cart in CartModel.objects:
                    carts.append({"rfid": carts.rfid})
                return carts, 200
            
        else:
            try:
                validate_rfid(rfid)
                cart = CartModel.objects.get(rfid=rfid)
            except TypeError:
                return {
                    "message": "RFID in wrong format"
                }
            except DoesNotExist:
                return {
                    "message": "Cart not found"
                }
            else:
                return {
                    'cart': cart['rfid']
                }, 200
    
    def post(self):
        try:
            post_data = request.get_json()
            cart_rfid = post_data['rfid']
            validate_rfid(cart_rfid)
            cart = CartModel()
            cart.rfid = cart_rfid
            cart.save()
        except TypeError:
            return {
                "message": "RFID in wrong format"
            }, 400
        else:
            return {
                'message': f'Cart {cart_rfid} successfully added'
            }, 200

    def delete(self, rfid):
        try:
            validate_rfid(rfid)
            cart = CartModel.objects.get(rfid=rfid)
            cart.delete()
        except TypeError:
            return {
                "message": "RFID in wrong format"
            }
        except DoesNotExist:
            return {
                "message": "Cart not found"
            }
        else:
            return {
                'cart': f'Cart {rfid} successfully removed'
            }, 200
    
    def put(self, rfid):
        try:
            post_data = request.get_json()
            new_rfid = post_data['rfid']

            validate_rfid(rfid)
            cart = CartModel.objects.get(rfid=rfid)

            cart.rfid = new_rfid
            cart.save()
        except TypeError:
            return {
                "message": "RFID in wrong format"
            }
        except DoesNotExist:
            return {
                "message": "Cart not found"
            }
        else:
            return {
                'cart': f'Cart {rfid} successfully updated to {new_rfid}'
            }, 200

class Purchase(Resource):
    def post(self):
        try:
            post_data = request.get_json()

            validate_rfid(post_data['cart'])
            cart = CartModel.objects.get(rfid=post_data['cart'])
            
            purchase = PurchaseModel()
            purchase.user_id = post_data['user_id']
            purchase.state = post_data['state']
            items_list = []
            for item in post_data['items']:
                validate_rfid(item)
                get_item_url = PRODUCTS_API + f"item/{item}"
                item = http_request(get_item_url, "get")
                # print(item,file=sys.stderr)
                items_list.append(item)
            purchase.purchased_products = items_list
            purchase.save()
            purchase.update(add_to_set__purchased_products=items_list)
        except TypeError:
            return {
                "message": "RFID in wrong format"
            }, 400
        except HTTPError as http_error:
            return {
                "message": "Item not found"
            }, 404
        except DoesNotExist:
            return {
                "message": "Cart not found"
            }, 404
        else:
            return {
                'message': "purchase created"
            }, 200



api.add_resource(Cart, '/api/cart/<rfid>',
                 endpoint="cart",
                 methods=['GET', 'DELETE', 'PUT'])
# https://github.com/flask-restful/flask-restful/issues/114
api.add_resource(Cart, '/api/cart/',
                 endpoint="carts",
                 methods=['GET', 'POST'])
api.add_resource(Purchase, '/api/purchase/',
                 endpoint="purchase",
                 methods=['POST'])
