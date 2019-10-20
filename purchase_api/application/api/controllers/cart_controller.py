from application.api.models.cart_model import CartModel
from mongoengine.errors import NotUniqueError
from application.api.utils import (
    db_utils,
    validators,
    data_formatter
)


def save_cart(cart_rfid):
    validators.validate_rfid(cart_rfid)
    for cart_document in CartModel.objects:
        if cart_rfid == cart_document['rfid']:
            raise NotUniqueError(f"Cart with RFID {cart_rfid} already exists")
    cart = CartModel()
    cart.rfid = cart_rfid
    cart.save()


def update_cart(new_rfid, rfid):
    validators.validate_rfid(new_rfid)
    cart = db_utils.get_doc_by_attr(CartModel, "rfid", rfid)
    cart.rfid = new_rfid
    cart.save()


def delete_cart(rfid):
    validators.validate_rfid(rfid)
    cart = db_utils.get_doc_by_attr(CartModel, "rfid", rfid)
    cart.delete()


def get_all_carts(rfid):
    carts = []
    if not CartModel.objects:
        return carts, 200
    else:
        for cart in CartModel.objects:
            carts.append(data_formatter.build_cart_json(cart))
        return carts, 200
