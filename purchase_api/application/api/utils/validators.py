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
    STATES = ['ONGOING', 'PAYING', 'COMPLETED', 'ABORTED']

    logging.debug('State = {}'.format(state))

    if state in STATES:
        logging.debug('@@@ entrou no if')
        return True
    else:
        return False
