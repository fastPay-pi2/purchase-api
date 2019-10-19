import re

def validate_rfid(rfid):
    if(re.search(r'^[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-'
                r'[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-'
                r'[0-9a-fA-F]{2}$', rfid)):
        return True
    else:
        raise TypeError("RFID in wrong format!!!!!")

def validate_fields(json, *args):
    err = []
    if not json:
        err.append('Could not find any json for request')
        return err

    for arg in args:
        if arg not in json:
            err.append(arg)
    return err