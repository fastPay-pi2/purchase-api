def build_cart_json(cart):
    cart_dict = dict()
    cart_dict["_id"] = str(cart["id"])
    cart_dict["rfid"] = cart["rfid"]
    return cart_dict


def build_purchase_json(purchase):
    purchases_dict = dict()
    purchases_dict["_id"] = str(purchase["id"])
    purchases_dict["user_id"] = str(purchase["user_id"])
    purchases_dict["state"] = purchase["state"]
    purchases_dict["date"] = str(purchase["date"])
    purchases_dict["value"] = str(purchase["value"])
    purchases_dict["purchased_products"] = purchase["purchased_products"]
    # TODO bug when access cart id of a deleted cart
    purchases_dict["cart"] = str(purchase["cart"])
    return purchases_dict


def format_message(message, status=500):
    if isinstance(message, dict) or isinstance(message, list):
        return message, status

    if status == 200:
        message = {'msg': message}
    else:
        message = {'error': message}

    return message, status


def items_to_products(items):
    '''
    Receives a list of repeated items and returns
    a list of products with the quantity of items
    '''

    products_ids = dict()  # key = productid, value = quantity
    products = []
    for i in items:
        if i['productid'] in products_ids.keys():
            products_ids[i['productid']].append(i['rfid'])
        else:
            products_ids[i['productid']] = [i['rfid']]
            products.append(i)
    for i in products:
        if 'rfid' in i:
            del i['rfid']

        i['rfids'] = products_ids[i['productid']]
        i['quantity'] = len(products_ids[i['productid']])

    return products


def structure_repeated_products(purchases):
    all_products = []
    for i in purchases:
        if i['state'] == 'COMPLETED':
            all_products += i['purchased_products']

    purchased_products = dict()  # key=productname, value=list of products
    for i in all_products:
        if 'rfids' in i:
            del i['rfids']

        product_name = i['productname']
        if product_name in purchased_products.keys():
            purchased_products[product_name]['quantity'] += i['quantity']
        else:
            purchased_products[product_name] = i

    purchased_products = [purchased_products[x] for x in purchased_products]

    return purchased_products
