from application.api import init_db
import mongoengine


class PurchaseModel(mongoengine.Document):
    init_db()
    user_id = mongoengine.IntField(required=True)
    state = mongoengine.StringField(
        max_length=10,
        choices=['PENDING', 'ABORTED', 'COMPLETED'],
        required=True
    )
    date = mongoengine.DateTimeField(default=None,
                                     required=False)
    purchased_products = mongoengine.ListField(mongoengine.DictField(),
                                               required=False)
    cart = mongoengine.ObjectIdField(required=True)
    meta = {
        'db_alias': 'purchase',
        'collection': 'Purchase'
    }
