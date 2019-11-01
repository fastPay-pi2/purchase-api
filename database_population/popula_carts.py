import requests
import logging
import sys
import os
from popula_purchases import generate_rfids_list

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


def build_cart_json(cart):
    cart_json = {
        "rfid": cart
    }
    return cart_json


def create_carts(carts_number, carts_list, table):
    """
    Create items in database
    >>> Params:
    items_number: Integer -> number of items in database
    rfids_list: List of Strings -> List with rfids in accepted format
    table: String -> Indicate table name. Should be passed 'item'
    """
    for i in range(0, carts_number):
        try:
            cart_json = build_cart_json(carts_list[i])
            requests.post(f'{PURCHASE_API_URL}/{table}/', json=cart_json)
            logging.info(f'{table.upper()} successfully added')
        except Exception as ex:
            logging.error(f'An unmapped exception occured')
            logging.error(ex)
            sys.exit()


def main():
    carts_number = 30
    carts_list = generate_rfids_list(carts_number, True)
    create_carts(carts_number, carts_list, "cart")


if __name__ == '__main__':
    main()
