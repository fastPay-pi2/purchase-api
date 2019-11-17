from application.api.models import PurchaseModel
from application.api.utils import validators
from collections import Counter
import logging

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(
    # filename='logfile.txt',
    # filemode='a',
    level=logging.DEBUG,
    format=FORMAT
)


def purchase_validation(data):
    cart_rfid = data['cart']

    if 'items' not in data:
        return cancel_purchase(cart_rfid)
    else:
        items = data['items']

    cart_purchases = PurchaseModel.objects.filter(
        cart=cart_rfid,
        state='COMPLETED'
    ).order_by('-date')

    if cart_purchases:
        last_purchase = cart_purchases[0]
    else:
        err = 'Could not find any purchase for cart'
        return err, 404

    items = Counter(items)  # dict -> key: barcode, value: quantity
    missing_products = []
    for product in last_purchase['purchased_products']:
        quantity = product['quantity']
        barcode = product['barcode']

        missing_prod = dict()
        if quantity > items[barcode]:
            missing_prod['name'] = product['productname']
            missing_prod['purchase_quantity'] = product['quantity']
            missing_prod['missing'] = quantity - items[barcode]
            missing_products.append(missing_prod)
        elif quantity < items[barcode]:
            err = ('Someone actually bought a product and left it: '
                   f'{product["productname"]} -> {barcode}')
            logging.error(err)

    response = dict()
    if missing_products:
        response['missing_products'] = missing_products
        return response, 418
    else:
        return "It's all good", 200


def cancel_purchase(cart_rfid):
    states_to_search = ['ONGOING', 'PAYING']
    pending_purchase = PurchaseModel.objects.filter(
        cart=cart_rfid,
        state__in=states_to_search
    )

    res, status = validators.validate_existing_purchase(pending_purchase)
    if status != 200:
        return res, status
    else:  # res = 1 purchase
        purchase = res
        purchase.state = 'ABORTED'
        purchase.purchased_products = []
        purchase.save()
        return 'Purchase successfully cancelled', 200
