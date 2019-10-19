from mongoengine.errors import DoesNotExist, NotUniqueError
import re

# def http_request(url, request_type, data=None):
#     headers = {
#         "Content-Type": "application/json"
#     }
#     try:
#         if request_type == "get":
#             response = get(url, headers=headers)
#         elif request_type == "post":
#             response = post(url, headers=headers,
#                             data=json.dumps(data))
#         elif request_type == "delete":
#             response = delete(url, headers=headers)
#         elif request_type == "put":
#             response = put(url, headers=headers,
#                            data=json.dumps(data))
#         response.raise_for_status()
#     except HTTPError as http_error:
#         raise HTTPError()
#     else:
#         resp_json = response.json()
#         return resp_json

def handle_exceptions(method, success_message, *args):
    try:
        if method:
            method(*args)
    except TypeError as err:
        return format_message(str(err), 400)
    except NotUniqueError as err:
        return format_message(str(err), 400)
    except IndexError as err:
        return format_message(str(err), 404)
    except DoesNotExist as err:
        return format_message(str(err), 404)
    else:
        return format_message(success_message, 200)

def format_message(message, status=500):
    if isinstance(message, dict):
        return message, status

    if status == 200:
        message = {'msg': message}
    else:
        message = {'error': message}
    
    return message, status

def validate_rfid(rfid):
    if(re.search(r'^[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                r'[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                r'[0-9A-F]{2}$', rfid)):
        return True
    else:
        raise TypeError("RFID in wrong format")



def db_dump():
    all_carts = get_all_collection_docs(CartModel)
    carts = build_cart_json(all_carts)
    all_purchases = get_all_collection_docs(PurchaseModel)
    purchases = build_purchase_json(all_purchases)
    return {
        "cart": carts,
        "purchase": purchases
    }

