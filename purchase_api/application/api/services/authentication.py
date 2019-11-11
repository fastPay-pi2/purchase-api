import requests

AUTH_URL = 'http://authentication_app:3001/check'


def authenticate(request):
    if 'Authorization' not in request:
        return 'Request unauthorized', 401

    token = request['Authorization']
    header = {
        'Authorization': token
    }

    r = requests.get(AUTH_URL, headers=header)
    if r.status_code == 200:
        return None, 200
    else:
        return 'Request unauthorized', 401
