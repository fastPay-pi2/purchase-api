from application.api.models.purchase_model import PurchaseModel
from application.api.models.cart_model import CartModel
from datetime import datetime
from requests import get
import os
from application.api.utils import (
    db_utils,
    validators,
    data_formatter
)

PRODUCTS_API = os.getenv("PRODUCTS_API", "")


def start_purchase(data):
    try:
        validators.validate_rfid(data['cart_id'])
        cart = db_utils.get_doc_by_attr(CartModel, "rfid", data['cart_id'])

        purchase = PurchaseModel()
        purchase.user_id = data['user_id']
        purchase.cart = cart['id']
        purchase.state = 'PENDING'
        purchase.purchased_products = []
        purchase_id = purchase.save()
        msg = f'Purchase for {purchase_id["user_id"]} successfully created'
        return {
            "msg": msg, 
            "id": f'{str(purchase_id["id"])}'
        }, 200
    except Exception as err:
        return {'err': str(err)}


def update_purchase(data, purchase_id):
    new_state = data['state']
    for item in data['items']:
        validators.validate_rfid(item)
    product_items = {
        "rfids": data["items"]
    }
    beautiful_item_url = PRODUCTS_API + f"beautifulitems"
    beautiful_items = get(beautiful_item_url, json=product_items).json()

    PurchaseModel.objects(id=purchase_id).update(
        set__state=new_state,
        set__purchased_products=beautiful_items,
        set__date=datetime.now()
    )


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