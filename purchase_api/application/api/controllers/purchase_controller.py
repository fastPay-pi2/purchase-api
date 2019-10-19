from application.api.models.purchase_model import PurchaseModel 

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
        beautiful_item = get(beautiful_item_url, json=product_items)
        items_list = beautiful_item.json()
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

def post_purchase(post_data):
    success_message = save_purchase(post_data)
    return handle_exceptions(None, success_message)

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
