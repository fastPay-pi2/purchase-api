from application.api.models import CartModel, PurchaseModel
from datetime import datetime, timedelta
from requests import get
import logging
import os
from application.api.utils import (
    validators,
    data_formatter
)

PRODUCTS_API = os.getenv("PRODUCTS_API", "")
BEAUTIFUL_ITEMS_URL = PRODUCTS_API + "beautifulitems"

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(
    # filename='logfile.txt',
    # filemode='a',
    level=logging.DEBUG,
    format=FORMAT
)


def start_purchase(data):
    # TODO validate cart RFID format
    rfid = data['cart_id']
    cart = CartModel.objects.get(rfid=rfid)

    err = check_pending_purchase(data['user_id'])
    if err:
        return err, 400

    err = check_cart_in_use(cart)
    if err:
        return err, 400

    purchase = PurchaseModel()
    purchase.user_id = data['user_id']
    purchase.cart = cart['id']
    purchase.state = 'ONGOING'
    purchase.purchased_products = []
    purchase.save()

    response = dict()
    response['msg'] = 'Purchase for {} successfully created'.format(
        purchase["user_id"]
    )
    response['id'] = str(purchase['id'])

    return response, 200


def server_update_purchase(data):
    items = data['items']  # TODO validate RFIDs
    cart_rfid = identify_cart_from_items(items)

    # If it does not exist, db raises an exception
    cart = CartModel.objects.get(rfid=cart_rfid)
    purchase = PurchaseModel.objects.get(cart=cart['id'], state='ONGOING')

    product_items = dict()
    product_items['rfids'] = data['items']

    beautiful_items = get(BEAUTIFUL_ITEMS_URL, json=product_items).json()
    value = sum([x['productprice'] for x in beautiful_items])

    purchase.update(
        set__state='PAYING',
        set__purchased_products=beautiful_items,
        set__value=value
    )

    logging.debug('entrou aqui')
    response = f'Purchase {str(purchase["id"])} sucssessfully updated'
    logging.debug('entrou aqui 2')
    return response, 200


def user_update_purchase(data, user_id):
    purchase = PurchaseModel.objects.get(user_id=user_id, state='PAYING')

    UTC_OFFSET = 3  # BRASÍLIA UTC
    time = datetime.now() - timedelta(hours=UTC_OFFSET)

    new_state = data['new_state']
    is_valid = validators.validate_state(new_state)

    if is_valid:
        purchase.update(
            set__state=new_state,
            set__date=time
        )
        response = f'Purchase {str(purchase["id"])} sucssessfully updated'
        return response, 200
    else:
        return 'Invalid state', 400


def delete_purchase(user_id):
    purchases = PurchaseModel.objects(user_id=user_id)
    for p in purchases:
        p.delete()

    response = f'Purchases for the user {user_id} successfully deleted'
    return response, 200


def get_purchases(user_id):
    if user_id:
        purchases = PurchaseModel.objects(user_id=user_id)
        if not purchases:
            return 'There are no purchases for user', 404
    else:
        purchases = PurchaseModel.objects

    response = []
    for p in purchases:
        response.append(data_formatter.build_purchase_json(p))
    return response, 200


def check_pending_purchase(user_id):
    user_purchases = PurchaseModel.objects(user_id=user_id)
    states = ['ONGOING', 'PAYING']  # Pending states
    pending_purchases = [x for x in user_purchases if x['state'] in states]
    if pending_purchases:
        err = 'There is a pending purchase'
        return err
    else:
        return None


def check_cart_in_use(cart):
    used_carts = PurchaseModel.objects(state='ONGOING', cart=cart['id'])
    if used_carts:
        err = 'Cart already being used in another purchase'
        return err
    else:
        return None


def identify_cart_from_items(items):
    carts = CartModel.objects.all()
    cart_rfids = []
    for cart in carts:
        cart_rfids.append(str(cart['rfid']))

    cart_rfid = [x for x in items if x in cart_rfids]
    if len(cart_rfid) == 1:
        cart_rfid = cart_rfid[0]
        items.remove(cart_rfid)
    elif len(cart_rfid) > 1:
        raise Exception('More than 1 cart was found')
    else:
        raise Exception('It was not possible to find a cart')

    return cart_rfid
