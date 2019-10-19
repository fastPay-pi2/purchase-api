import re
from requests import get, post, delete, put
from requests.exceptions import HTTPError
import json
import sys
from application.api.models import CartModel, PurchaseModel
from mongoengine.errors import DoesNotExist, NotUniqueError
from mongoengine.errors import NotUniqueError
import os
import json

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

def save_purchase(post_data):
    try:
        validate_rfid(post_data['cart'])
        cart = get_doc_by_attr(CartModel, "rfid", post_data['cart'] )
        
        purchase = PurchaseModel()
        purchase.user_id = post_data['user_id']
        purchase.state = post_data['state']

        items_list = []
        for item in post_data['items']:
            validate_rfid(item)
        product_items = { 
            "rfids": post_data["items"]
        }
        beautiful_item_url = PRODUCTS_API + f"beautifulitems"
        beautiful_item = get(beautiful_item_url, json=product_items)
        items_list = beautiful_item.json()
        cart = get_doc_by_attr(CartModel, "rfid", post_data["cart"])
    except IndexError:
        raise IndexError("Item not Found")
    else:
        purchase.purchased_products = items_list
        purchase.cart = cart['id']
        purchase_id = purchase.save()
        return {
            'message': f"purchase {purchase_id['id']} created"
        }

def post_purchase(post_data):
    success_message = save_purchase(post_data)
    return handle_exceptions(None, success_message)


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

def update_purchase(post_data, purchase_id):
    new_state = post_data['state']
    items_list = []
    for item in post_data['items']:
            validate_rfid(item)
    product_items = { 
        "rfids": post_data["items"]
    }
    beautiful_item_url = PRODUCTS_API + f"beautifulitems"
    beautiful_item = get(beautiful_item_url, json=product_items)
    items_list = beautiful_item.json()
    # purchase.state = new_state
    # purchase.purchased_products.append(items_list)
    a = {"state": new_state, "purchased_products": items_list}
    PurchaseModel.objects(id=purchase_id).update(set__state=new_state,
                                                 set__purchased_products=items_list)
    # PurchaseModel.update_one(purchase, a)

def get_all_collection_docs(model_name):
    all_docs = []
    if not model_name.objects:
        pass
    else:
        for doc in model_name.objects:
            document = doc.to_json()
            doc_json = json.loads(document)
            all_docs.append(doc_json)
    return all_docs

def build_cart_json(all_carts):
    carts = []
    cart_dict = {}
    for cart in all_carts:
        cart_dict["_id"] = cart["_id"]["$oid"] 
        cart_dict["rfid"] = cart["rfid"]
        carts.append(cart_dict)
    return carts

def build_purchase_json(all_purchases):
    purchases = []
    purchases_dict = {}
    for purchase in all_purchases:
        purchases_dict["_id"] = purchase["_id"]["$oid"]
        purchases_dict["user_id"] = purchase["user_id"]
        purchases_dict["state"] = purchase["state"]
        purchases_dict["date"] = purchase["date"]["$date"]
        purchases_dict["purchased_products"] = purchase["purchased_products"]
        purchases_dict["cart"] = purchase["cart"]["$oid"]
    return purchases_dict

def db_dump():
    all_carts = get_all_collection_docs(CartModel)
    carts = build_cart_json(all_carts)
    all_purchases = get_all_collection_docs(PurchaseModel)
    purchases = build_purchase_json(all_purchases)
    return {
        "cart": carts,
        "purchase": purchases
    }

def handle_exceptions(method, success_message, *args):
    try:
        if method:
            method(*args)
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
