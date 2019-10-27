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
    try:
        validators.validate_rfid(data['cart_id'])
        cart = db_utils.get_doc_by_attr(CartModel, "rfid", data['cart_id'])

        logging.debug(f'cart = {cart.to_json()}')

        purchase = PurchaseModel()
        purchase.user_id = data['user_id']
        purchase.cart = cart
        purchase.state = 'PENDING'
        purchase.purchased_products = []

        logging.debug(f'purchase = {purchase.to_json()}')

        purchase_id = purchase.save()

        msg = f'Purchase for {purchase_id["user_id"]} successfully created'
        return {
            "msg": msg,
            "id": f'{str(purchase_id["id"])}'
        }, 200
    except Exception as err:
        return {'err': str(err)}


# TODO change logic to update searching a cart through list of RFIDS
def update_purchase(data, purchase_id):
    new_state = data['state']
    for item in data['items']:
        validators.validate_rfid(item)
    product_items = {
        "rfids": data["items"]
    }
    beautiful_item_url = PRODUCTS_API + f"beautifulitems"
    beautiful_items = get(beautiful_item_url, json=product_items).json()
    value = sum([x['productprice'] for x in beautiful_items])

    UTC_OFFSET = 3
    time = datetime.now() - timedelta(hours=UTC_OFFSET)

    # TODO update by user_id and state = PENDING
    rows = PurchaseModel.objects(id=purchase_id).update(
        set__state=new_state,
        set__purchased_products=beautiful_items,
        set__date=time,
        set__value=value
    )

    if rows <= 0:
        raise Exception('Could not find the purchase')
    elif rows > 1:
        raise Exception('More than 1 id for purchase')


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
