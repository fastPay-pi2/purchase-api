from flask import Blueprint, request
from flask_restful import Resource, Api
from application.api.models import CartModel
from application.api.controller import CartControler
from mongoengine.errors import DoesNotExist   
import sys

views_blueprint = Blueprint('views', __name__)
api = Api(views_blueprint)


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
                cart_controller = CartControler()
                cart_controller.validate_rfid(rfid)
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
            cart_controller = CartControler()
            cart_controller.validate_rfid(cart_rfid)
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
            cart_controller = CartControler()
            cart_controller.validate_rfid(rfid)
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

            cart_controller = CartControler()
            cart_controller.validate_rfid(rfid)
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

api.add_resource(Cart, '/api/cart/<rfid>',
                 endpoint="cart",
                 methods=['GET', 'DELETE', 'PUT'])
api.add_resource(Cart, '/api/cart/',
                 endpoint="carts",
                 methods=['GET', 'POST'])
