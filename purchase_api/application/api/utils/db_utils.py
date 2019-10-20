from application.api.models.cart_model import CartModel
from application.api.models.purchase_model import PurchaseModel
from application.api.utils.data_formatter import build_cart_json, \
                                                 build_purchase_json
import json


def get_doc_by_attr(model_name, attr, value):
    document = model_name.objects.get(**{attr: value})
    return document


def get_all_collection_docs(model_name):
    all_docs = []
    if not model_name.objects:
        pass
    else:
        for doc in model_name.objects:
            document = doc.to_json()
            doc_json = json.loads(document)
            all_docs.append(doc_json)
    return all_docs


def db_dump():
    all_carts = get_all_collection_docs(CartModel)
    carts = build_cart_json(all_carts)
    all_purchases = get_all_collection_docs(PurchaseModel)
    purchases = build_purchase_json(all_purchases)
    return {
        "cart": carts,
        "purchase": purchases
    }
