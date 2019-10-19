from application.api import init_db
from application.api.models.purchase_model import PurchaseModel
import mongoengine
import sys
import datetime

class CartModel(mongoengine.Document):
    init_db()
    purchase = mongoengine.ReferenceField(PurchaseModel)
    rfid = mongoengine.StringField(required=True,
                                   max_length=20,
                                   unique=True)
    meta = {
        'db_alias': 'purchase',
        'collection': 'Cart'
    }