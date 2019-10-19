def build_cart_json(cart):
    cart_dict = dict()
        # cart_dict["_id"] = cart["_id"]["$oid"]
    cart_dict["rfid"] = cart["rfid"]
    return cart_dict

def build_purchase_json(purchase):
    # purchases = []
    purchases_dict = dict()
    # for purchase in all_purchases:
        # purchases_dict["_id"] = purchase["_id"]["$oid"]
        # return {'msg': str(purchase)}
    purchases_dict["user_id"] = purchase["user_id"]
    purchases_dict["state"] = purchase["state"]
    purchases_dict["date"] = str(purchase["date"])
    purchases_dict["purchased_products"] = purchase["purchased_products"]
    purchases_dict["cart"] = str(purchase["cart"])
    return purchases_dict

def format_message(message, status=500):
    if isinstance(message, dict):
        return message, status

    if status == 200:
        message = {'msg': message}
    else:
        message = {'error': message}
    
    return message, status