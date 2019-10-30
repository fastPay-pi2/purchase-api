from application.api.models import CartModel
from application.api.utils import (
    # validators,
    data_formatter
)


# TODO Validate RFIDs
def save_cart(cart_rfid):
    # validators.validate_rfid(new_rfid)
    cart = CartModel()
    cart.rfid = cart_rfid
    cart.save()

    return f'Cart {cart["rfid"]} successfully created', 200


def get_carts(rfid):
    if rfid:
        cart = CartModel.objects.get(rfid=rfid)
        cart = data_formatter.build_cart_json(cart)
        return cart, 200
    else:
        carts = []
        for cart in CartModel.objects:
            carts.append(data_formatter.build_cart_json(cart))
        return carts, 200


def update_cart(rfid, new_rfid):
    # validators.validate_rfid(new_rfid)
    cart = CartModel.objects.get(rfid=rfid)
    cart.rfid = new_rfid
    cart.save()

    return f'Cart {cart["rfid"]} successfully updated', 200


def delete_cart(rfid):
    # validators.validate_rfid(rfid)
    cart = CartModel.objects.get(rfid=rfid)
    cart.delete()

    return 'Cart successfully deleted', 200
