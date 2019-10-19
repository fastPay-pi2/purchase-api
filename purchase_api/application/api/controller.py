import re
from requests import get, post, delete, put
from requests.exceptions import HTTPError
import json
import sys
from application.api.models.cart_model import CartModel
from application.api.models.purchase_model import PurchaseModel 
from mongoengine.errors import DoesNotExist, NotUniqueError
from mongoengine.errors import NotUniqueError
import os
import json

from application.api.utils import handle_exceptions, validate_rfid

PRODUCTS_API = os.getenv("PRODUCTS_API", "")


def get_doc_by_attr(model_name, attr, value):
    document = model_name.objects.get(**{attr: value})
    return document

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
