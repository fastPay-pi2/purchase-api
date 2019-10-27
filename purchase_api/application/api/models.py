from application.api import init_db
import mongoengine


class CartModel(mongoengine.Document):
    init_db()
    # purchase = mongoengine.ReferenceField(PurchaseModel)
    rfid = mongoengine.StringField(required=True,
                                   max_length=20,
                                   unique=True)
    meta = {
        'db_alias': 'purchase',
        'collection': 'Cart'
    }


class PurchaseModel(mongoengine.Document):
    init_db()
    user_id = mongoengine.StringField(max_length=30, required=True)
    state = mongoengine.StringField(
        max_length=10,
        choices=['ONGOING', 'PAYING', 'ABORTED', 'COMPLETED'],
        required=True
    )
    date = mongoengine.DateTimeField(default=None,
                                     required=False)
    purchased_products = mongoengine.ListField(mongoengine.DictField(),
                                               required=False)
    cart = mongoengine.ReferenceField(CartModel, required=True)
    value = mongoengine.FloatField(default=0, min_value=0,
                                   required=False)
    meta = {
        'db_alias': 'purchase',
        'collection': 'Purchase'
    }
