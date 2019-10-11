import re

def validate_rfid(rfid):
    if(re.search(r'^[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                r'[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                r'[0-9A-F]{2}$', rfid)):
        return True
    else:
        raise TypeError