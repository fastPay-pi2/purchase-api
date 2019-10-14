import re
from requests import get, post, delete, put
from requests.exceptions import HTTPError
import json
import sys
from application.api.models import CartModel, PurchaseModel
from mongoengine.errors import DoesNotExist, NotUniqueError
from mongoengine.errors import NotUniqueError
import os


PRODUCTS_API = os.getenv("PRODUCTS_API", "")

def validate_rfid(rfid):
    if(re.search(r'^[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                r'[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                r'[0-9A-F]{2}$', rfid)):
        return True
    else:
        raise TypeError("RFID in wrong format")

def http_request(url, request_type, data=None):
    headers = {
        "Content-Type": "application/json"
    }
    try:
        if request_type == "get":
            response = get(url, headers=headers)
        elif request_type == "post":
            response = post(url, headers=headers,
                            data=json.dumps(data))
        elif request_type == "delete":
            response = delete(url, headers=headers)
        elif request_type == "put":
            response = put(url, headers=headers,
                           data=json.dumps(data))
        response.raise_for_status()
    except HTTPError as http_error:
        raise HTTPError()
    else:
        resp_json = response.json()
        return resp_json

def get_doc_by_attr(model_name, attr, value):
    document = model_name.objects.get(**{attr: value})
    return document

def save_cart(cart_rfid):
    validate_rfid(cart_rfid)
    for cart_document in CartModel.objects:
        if cart_rfid == cart_document['rfid']:
            raise NotUniqueError(f"Cart with RFID {cart_rfid} already exists")
    cart = CartModel()
    cart.rfid = cart_rfid
    cart.save()

def update_cart(new_rfid, rfid):
    validate_rfid(new_rfid)
    cart = get_doc_by_attr(CartModel, "rfid", rfid)
    cart.rfid = new_rfid
    cart.save()

def post_purchase(post_data):
    try:
        validate_rfid(post_data['cart'])
        cart = get_doc_by_attr(CartModel, "rfid", post_data['cart'] )
        
        purchase = PurchaseModel()
        purchase.user_id = post_data['user_id']
        purchase.state = post_data['state']

        items_list = []
        for item in post_data['items']:
            validate_rfid(item)
            get_item_url = PRODUCTS_API + f"item/{item}"
            item = http_request(get_item_url, "get")
            items_list.append(item[0]['rfid'])
    except IndexError:
        raise IndexError("Item not Found")
    else:
        purchase.purchased_products = items_list
        purchase.save()


def delete_cart(rfid):
    validate_rfid(rfid)
    cart = get_doc_by_attr(CartModel,"rfid", rfid)
    cart.delete()

def put_cart(post):
    post_data = request.get_json()
    new_rfid = post_data['rfid']
    update_cart(new_rfid, rfid)

def get_all_carts(rfid):
    carts = []
    if not CartModel.objects:
        return carts, 200
    else:
        for cart in CartModel.objects:
            carts.append({"rfid": cart['rfid']})
        return carts, 200 


def handle_exceptions(method, success_message, *args):
    try:
        if len(args) == 1:
            method(args[0])
        elif len(args) == 2:
            method(args[0], args[1])
        elif len(args) == 3:
            method(args[0], args[1], args[2])
    except TypeError as err:
        return {
                "message": str(err)
                }, \
               400
    except NotUniqueError as err:
        return {
                "message": str(err)
                }, \
               400
    except IndexError as err:
        return {
                "message": str(err)
                }, \
               404
    except DoesNotExist as err:
        return {
                "message": str(err)
                }, \
               404
    else:
        return success_message, 200
