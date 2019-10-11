import re

class CartControler():
    def validate_rfid(self, rfid):
        if(re.search(r'^[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                    r'[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                    r'[0-9A-F]{2}$', rfid)):
            return True
        else:
            raise TypeError