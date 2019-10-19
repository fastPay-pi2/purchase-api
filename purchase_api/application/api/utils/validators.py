import re

def validate_rfid(rfid):
    if(re.search(r'^[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-'
                r'[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-'
                r'[0-9a-fA-F]{2}$', rfid)):
        return True
    else:
        raise TypeError("RFID in wrong format!!!!!")

def validate_fields(json, *args):
    if not json:
        return False

    for arg in args:
        if arg not in json:
            return False
    return True