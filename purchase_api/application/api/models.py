import mongoengine
from application.api import init_db
import sys
import datetime

class PurchaseModel(mongoengine.Document):
    init_db()
    user_id = mongoengine.IntField(required=True)
    state = mongoengine.StringField(max_length=10,
                                    choices=['PENDING', 'ABORTED', 'FINISHED'],
                                    required=True)
    date = mongoengine.DateTimeField(default=datetime.datetime.utcnow,
                                     required=True)
    purchased_products = mongoengine.ListField(mongoengine.DictField(),
                                               required=True)
    cart = mongoengine.ObjectIdField(required=True)
    meta = {
        'db_alias': 'purchase',
        'collection': 'Purchase'
    }

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
