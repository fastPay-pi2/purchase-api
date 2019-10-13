import mongoengine
from application.api import init_db
import sys
import datetime

class CartModel(mongoengine.Document):
    init_db()
    rfid = mongoengine.StringField(required=True, max_length=20)
    meta = {
        'db_alias': 'purchase',
        'collection': 'Cart'
    }

class PurchaseModel(mongoengine.Document):
    init_db()
    user_id = mongoengine.IntField(required=True)
    state = mongoengine.StringField(max_length=10,
                                    choices=['PENDING', 'ABORTED', 'FINISHED'])
    date = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    purchased_products = mongoengine.ListField(mongoengine.StringField(max_length=20))
    meta = {
        'db_alias': 'purchase',
        'collection': 'Purchase'
    }