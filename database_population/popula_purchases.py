import requests
import logging
import sys
import os
import itertools
import random

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(
    # filename='logfile.txt',
    # filemode='a',
    level=logging.DEBUG,
    format=FORMAT
)


PRODUCT_API_URL = os.getenv("PRODUCT_API_URL", "http://localhost:3000")
PURCHASE_API_URL = os.getenv("PURCHASE_API_URL", "http://localhost:5000")
# PRODUCT_API_URL = 'http://localhost:3000'


def get_all_request(table):
    r = requests.get(f'{PRODUCT_API_URL}/{table}')
    if r.status_code == 200:
        categories = r.json()
    elif r.status_code == 404:
        categories = []
    else:
        logging.error(f'Error on requesting PRODUCT API: {r.status_code}')
        raise Exception
    return categories


def generate_rfids_list(items_number, cart=False):
    """
    Create rfids list in accepted format
    >>> Params:
    items_number: Integer -> number of products in database
    """
    if cart:
        allowed_numbers = list(range(1, 10))
    else:
        allowed_numbers = list(range(0, 10))
    allowed_numbers_str = [str(number) for number in allowed_numbers]

    # uppercase A - F indexes
    allowed_characters = list(map(chr, range(65, 71)))
    allowed_digits = allowed_numbers_str + allowed_characters

    rfids_list = list(map(''.join, itertools.islice(itertools.product(
                                                     allowed_digits,
                                                     allowed_digits, ['-'],
                                                     allowed_digits,
                                                     allowed_digits, ['-'],
                                                     allowed_digits,
                                                     allowed_digits, ['-'],
                                                     allowed_digits,
                                                     allowed_digits, ['-'],
                                                     allowed_digits,
                                                     allowed_digits, ['-'],
                                                     allowed_digits,
                                                     allowed_digits, ['-'],
                                                     allowed_digits,
                                                     allowed_digits),
                                                    items_number + 1)))
    return rfids_list


def generate_user_id_list(items_number):
    """
    Create rfids list in accepted format
    >>> Params:
    items_number: Integer -> number of products in database
    """
    allowed_numbers = list(range(2, 10))
    
    allowed_numbers_str = [str(number) for number in allowed_numbers]

    # lowercase a - z indexes
    allowed_characters = list(map(chr, range(97, 103)))
    allowed_digits = allowed_numbers_str + allowed_characters
    user_id_list = list(map(''.join, itertools.islice(
                                     itertools.combinations_with_replacement(
                                        allowed_digits, 24), items_number + 1)))
    return user_id_list

def return_random_items(random_range, rfids_list, items_number):
    items = []
    items_indexes = random.sample(range(1, items_number), random_range)
    for item in items_indexes:
        items.append(rfids_list[item])
    return items


def build_item_json(user_id, cart, state):
    """
    Build item json for post request.
    >>> Params:
    user_id: String -> Indicate user id
    cart: String -> Indicate cart id
    state: String -> Indicate the purchase state
    """
    item_json = {
        "user_id": str(user_id),
        "cart_id": cart,
        "state": state,
        "items": []
    }
    return item_json


def create_items(items_number, rfids_list, carts_list, 
                 user_id_list, carts_number, table):
    """
    Create items in database
    >>> Params:
    items_number: Integer -> number of items in database
    rfids_list: List of Strings -> List with rfids in accepted format
    user_id_list: List of Strings -> List with user_ids in accepted format
    carts_list: List of Strings -> List of carts id
    table: String -> Indicate table name. Should be passed 'purchase'
    """
    cart_index = 0
    for i in range(1, items_number + 1):
        try:
            user_items_number = 40
            # products bought by an user
            random_range = random.randint(1,
                                          user_items_number)
            user_items = return_random_items(random_range,
                                             rfids_list,
                                             items_number)

            if cart_index > 29:
                cart_index = 0


            post_json = {
                "user_id": user_id_list[i],
                "cart_id": carts_list[cart_index]
            }            
            post_req = requests.post(f'{PURCHASE_API_URL}/{table}/',
                                     json=post_json)
            user_items.append(carts_list[cart_index])

            server_put_json = {
                "items": user_items
            }
            server_put = requests.put(f'{PURCHASE_API_URL}/'
                         f'{table}/',
                         json=server_put_json)

            state_json = {
                "new_state": "COMPLETED"
            }
            user_put = requests.put(f'{PURCHASE_API_URL}/'
                         f'{table}/{user_id_list[i]}',
                         json=state_json)
            cart_index += 1
            logging.info(f'{table.upper()} successfully added')
        except Exception as ex:
            # logging.error(f'An unmapped exception occured')
            logging.error(ex)
            sys.exit()


def main():
    all_items = get_all_request('item')
    items_number = len(all_items)
    rfids_list = generate_rfids_list(items_number, False)
    carts_number = 30
    carts_list = generate_rfids_list(carts_number, True)

    user_id_list = generate_user_id_list(items_number)
    create_items(items_number, rfids_list, carts_list,
                 user_id_list, carts_number, "purchase")


if __name__ == '__main__':
    main()
