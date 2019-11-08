import logging
import re

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT
)


def validate_rfid(rfid):
    if(re.search(r'^[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-'
                 r'[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-'
                 r'[0-9a-fA-F]{2}$', rfid)):
        return True
    else:
        raise TypeError("RFID in wrong format")


def validate_fields(json, *args):
    err = []
    if not json:
        err.append('Could not find any json for request')
        return err

    for arg in args:
        if arg not in json:
            err.append(arg)
    return err


def validate_state(state):
    STATES = ['COMPLETED', 'ABORTED']

    logging.debug('State = {}'.format(state))

    if state in STATES:
        return True
    else:
        return False


def validate_existing_purchase(purchase):
    status = 200

    if len(purchase) == 1:
        res = purchase[0]
    elif len(purchase) > 1:
        status = 400
        res = 'More than 1 purchase found for user'
    elif len(purchase) == 0:
        status = 404
        res = 'It was not possible to find a purchase for user id'

    return res, status
