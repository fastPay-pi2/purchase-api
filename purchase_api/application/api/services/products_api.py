import requests
import logging
import os

PRODUCTS_API = os.getenv("PRODUCTS_API", "")
BEAUTIFUL_ITEMS_URL = PRODUCTS_API + "beautifulitems"
REMOVE_ITEMS_URL = PRODUCTS_API + "item"


def get_beautiful_items(product_items):
    r = requests.get(BEAUTIFUL_ITEMS_URL, json=product_items)
    beautiful_items = r.json()

    return beautiful_items


def delete_items(rfids_list):
    payload = dict()
    payload['rfids'] = rfids_list
    r = requests.delete(REMOVE_ITEMS_URL, json=payload)
    if r.status_code != 200:
        logging.error(r.text)
