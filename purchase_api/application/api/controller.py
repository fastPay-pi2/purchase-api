import re
from requests import get, post, delete, put
from requests.exceptions import HTTPError
import json
import sys

def validate_rfid(rfid):
    if(re.search(r'^[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                r'[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-'
                r'[0-9A-F]{2}$', rfid)):
        return True
    else:
        raise TypeError

def http_request(url, request_type, data=None):
    headers = {
        "Content-Type": "application/json"
    }
    try:
        if request_type == "get":
            response = get(url, headers=headers)
        elif request_type == "post":
            response = post(url, headers=headers,
                            data=json.dumps(data))
        elif request_type == "delete":
            response = delete(url, headers=headers)
        elif request_type == "put":
            response = put(url, headers=headers,
                           data=json.dumps(data))
        response.raise_for_status()
    except HTTPError as http_error:
        raise HTTPError()
    else:
        resp_json = response.json()
        return resp_json