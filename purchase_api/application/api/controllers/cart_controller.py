from application.api.models.cart_model import CartModel
from application.api.utils.validators import validate_rfid
from application.api.utils.db_utils import get_doc_by_attr
from application.api.utils.data_formatter import build_cart_json
from mongoengine.errors import NotUniqueError

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
            carts.append(build_cart_json(cart))
        return carts, 200 