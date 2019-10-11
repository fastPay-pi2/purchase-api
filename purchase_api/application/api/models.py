import mongoengine
from application.api import init_db
import sys

class CartModel(mongoengine.Document):
    init_db()
    rfid = mongoengine.StringField(required=True, max_length=20)
    meta = {
        'db_alias': 'purchase',
        'collection': 'Cart'
    }