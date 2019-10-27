from application.api.models import CartModel, PurchaseModel
from datetime import datetime, timedelta
from requests import get
import logging
import os
from application.api.utils import (
    db_utils,
    validators,
    data_formatter
)

PRODUCTS_API = os.getenv("PRODUCTS_API", "")

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(
    # filename='logfile.txt',
    # filemode='a',
    level=logging.DEBUG,
    format=FORMAT
)


def start_purchase(data):
    # validators.validate_rfid(data['cart_id'])
    rfid = data['rfid']
    cart = CartModel.objects.get(rfid=rfid)

    # logging.debug(f'cart = {cart.to_json()}')

    purchase = PurchaseModel()
    purchase.user_id = data['user_id']
    purchase.cart = cart
    purchase.state = 'ONGOING'
    purchase.purchased_products = []

    # logging.debug(f'purchase = {purchase.to_json()}')

    purchase_id = purchase.save()

    msg = f'Purchase for {purchase_id["user_id"]} successfully created'
    return {
        "msg": msg,
        "id": f'{str(purchase_id["id"])}'
    }, 200


def server_update_purchase(data):
    carts = CartModel.objects.all()
    cart_rfids = []
    for cart in carts:
        cart_rfids.append(str(cart['rfid']))

    # TODO validate RFIDs
    items = data['items']
    cart_rfid = [x for x in items if x in cart_rfids]

    if len(cart_rfid) == 1:
        cart_rfid = cart_rfid[0]
    elif len(cart_rfid) > 1:
        raise Exception('More than 1 cart was found')
    else:
        raise Exception('It was not possible to find a cart')

    # If it does not exist, db raises an exception
    cart = CartModel.objects.get(rfid=cart_rfid)
    purchase = PurchaseModel.objects(cart=cart, state='ONGOING')[0] # TODO change to get to take just 1

    product_items = dict()
    product_items['rfids'] = data['items']

    beautiful_item_url = PRODUCTS_API + f"beautifulitems"
    beautiful_items = get(beautiful_item_url, json=product_items).json()
    value = sum([x['productprice'] for x in beautiful_items])

    purchase.update(
        set__state='PAYING',
        set__purchased_products=beautiful_items,
        set__value=value
    )

    msg = f'Purchase {str(purchase["id"])} sucssessfully updated'
    return data_formatter.format_message(msg, 200)


def user_update_purchase(data, user_id):
    purchase = PurchaseModel.objects.get(user_id=user_id, state='PAYING')
    
    UTC_OFFSET = 3 # BRASÍLIA UTC
    time = datetime.now() - timedelta(hours=UTC_OFFSET)

    new_state = data['new_state']
    is_valid = validators.validate_state(new_state)

    if is_valid:
        purchase.update(
            set__state=new_state,
            set__date=time
        )
        msg = f'Purchase {str(purchase["id"])} sucssessfully updated'
        return data_formatter.format_message(msg, 200)
    else:
        return data_formatter.format_message('Invalid state', 400)

def delete_purchase(purchase_id):
    purchase = db_utils.get_doc_by_attr(PurchaseModel, "id", purchase_id)
    purchase.delete()


def get_purchases(user_id):
    if user_id:
        purchases = PurchaseModel.objects(user_id=user_id)
    else:
        purchases = PurchaseModel.objects

    response = []
    for p in purchases:
        response.append(data_formatter.build_purchase_json(p))
    return response
