from application.api.models.purchase_model import PurchaseModel
from application.api.models.cart_model import CartModel
from application.api.utils.db_utils import get_doc_by_attr
from application.api.utils.validators import validate_rfid
from application.api.utils.data_formatter import build_cart_json, build_purchase_json, format_message
from application.api.utils.handlers import handle_exceptions
from requests import get
import os
PRODUCTS_API = os.getenv("PRODUCTS_API", "")


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
        # beautiful_item = get(beautiful_item_url, json=product_items)
        # items_list = beautiful_item.json()
        items_list = [
            {
                'item1': 'eoq'
            }
        ]
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

import json
def start_purchase(data):
    try:
        validate_rfid(data['cart_id'])
        cart = get_doc_by_attr(CartModel, "rfid", data['cart_id'])

        purchase = PurchaseModel()
        purchase.user_id = data['user_id']
        purchase.cart = cart['id']
        purchase.state = 'PENDING'
        purchase.purchased_products = []
        purchase_id = purchase.save()
        return format_message(f'Purchase for {purchase_id["user_id"]} successfully created', 200)

    except Exception as err:
        return {'err': str(err)}


    try:
            
        cart = build_cart_json([cart])
        purchase = ''
        purchase = build_purchase_json([purchase_id])
    
    except Exception as err:
        return {'err':  str(err)}

    return {'cart': cart, 'purchase': purchase}

   
def post_purchase(post_data):
    success_message = f'Purchase successfully created'
    return handle_exceptions(start_purchase, success_message)
    # success_message = save_purchase(post_data)
    # return handle_exceptions(None, success_message)

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

def get_all_purchases():
    purchases = []
    if not PurchaseModel.objects:
        return purchases, 200
    else:
        for purchase in PurchaseModel.objects:
            purchases.append(build_purchase_json(purchase))
            # purchases.append(json.loads(purchase.to_json()))
        return purchases 