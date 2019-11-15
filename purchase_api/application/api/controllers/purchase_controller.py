from application.api.models import CartModel, PurchaseModel
from application.api.services import products_api
from tzlocal import get_localzone
from datetime import datetime
from decimal import Decimal
import logging
import pytz

from application.api.utils import (
    validators,
    data_formatter
)

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
    purchase.cart = cart['rfid']
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
    purchase = PurchaseModel.objects.filter(
        cart=cart['rfid'],
        state__in=['ONGOING', 'PAYING']
    )

    res, status = validators.validate_existing_purchase(purchase)
    if status == 200:
        purchase = res
    else:
        return res, status

    product_items = dict()
    product_items['rfids'] = list(set(data['items']))

    beautiful_items = products_api.get_beautiful_items(product_items)
    products = data_formatter.items_to_products(beautiful_items)
    value = sum([Decimal(str(x['productprice'])) for x in beautiful_items])

    purchase.update(
        set__state='PAYING',
        set__purchased_products=products,
        set__value=value
    )

    response = f'Purchase {str(purchase["id"])} successfully updated'
    return response, 200


def user_update_purchase(data, user_id):
    new_state = data['new_state']
    is_valid = validators.validate_state(new_state)
    if is_valid:
        # the state can only become 'completed' if it's in PAYING state
        if new_state == 'COMPLETED':
            states_to_search = ['PAYING']

        # the state can become 'aborted' at any time during the purchase
        elif new_state == 'ABORTED':
            states_to_search = ['ONGOING', 'PAYING']

        purchase = PurchaseModel.objects.filter(
            user_id=user_id,
            state__in=states_to_search
        )
    else:
        return 'Invalid state', 400

    res, status = validators.validate_existing_purchase(purchase)
    if status == 200:
        purchase = res
    else:
        return res, status

    purchased_rfids = []
    for purchased_products in purchase['purchased_products']:
        purchased_rfids += purchased_products['rfids']
        purchased_products['rfids'] = []

    if new_state == 'COMPLETED':
        products_api.delete_items(purchased_rfids)

    tz = get_localzone()
    local_dt = tz.localize(datetime.now(), is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    purchase.state = new_state
    purchase.date = utc_dt
    purchase.save()

    response = f'Purchase {str(purchase["id"])} successfully updated'
    return response, 200


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
    used_carts = PurchaseModel.objects(state='ONGOING', cart=cart['rfid'])
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
