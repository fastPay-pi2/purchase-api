from application.api.models import PurchaseModel

from application.api.utils import (
    validators,
    data_formatter
)


def purchase_dump(user_id):
    if user_id:
        return user_purchases_dump(user_id)

    purchases = PurchaseModel.objects()

    users = dict()
    for p in purchases:
        user_id = str(p['user_id'])
        if user_id in users.keys():
            users[user_id].append(p)
        else:
            users[user_id] = [p]

    response = []
    for user in users:
        u_products = data_formatter.structure_repeated_products(users[user])
        for p in u_products:
            p['user_id'] = user
        response += u_products

    return response, 200


def user_purchases_dump(user_id):
    user_purchases = PurchaseModel.objects(user_id=user_id)
    if not user_purchases:
        return 'There are no purchases for user', 404

    purchased_products = data_formatter.structure_repeated_products(
        user_purchases
    )
    return purchased_products, 200
