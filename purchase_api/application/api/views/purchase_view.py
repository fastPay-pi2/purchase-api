from application.api.services import authentication
from flask_restful import Resource, Api
from flask import Blueprint, request
from flask_cors import CORS

from application.api.utils import (
    validators,
    decorators
)
from application.api.controllers.purchase_controller import (
    server_update_purchase,
    user_update_purchase,
    delete_purchase,
    start_purchase,
    get_purchases
)

from application.api.controllers.dump_controller import (
    purchase_dump
)

from application.api.controllers.purchase_validation_controller import (
    purchase_validation
)

purchase_blueprint = Blueprint('views', __name__)
api = Api(purchase_blueprint)
CORS(purchase_blueprint)


class Purchase(Resource):
    @decorators.handle_exceptions
    def post(self):
        response, status = authentication.authenticate(request.headers)
        if status != 200:
            return response, status

        data = request.get_json()
        err = validators.validate_fields(data, 'user_id', 'cart_id')
        if err:
            err = f'Fields are missing: {", ".join(err)}'
            return err, 400
        else:
            response, status = start_purchase(data)
            return response, status

    @decorators.handle_exceptions
    def put(self, user_id=None):
        data = request.get_json()

        # endpoint for the user
        if user_id:
            response, status = authentication.authenticate(request.headers)
            if status != 200:
                return response, status

            err = validators.validate_fields(data, 'new_state')
            if err:
                err = f'Fields are missing: {", ".join(err)}'
                return err, 400
            else:
                response, status = user_update_purchase(data, user_id)
                return response, status
        # endpoint for the server
        else:
            err = validators.validate_fields(data, 'items')
            if err:
                err = f'Fields are missing: {", ".join(err)}'
                return err, 400
            else:
                response, status = server_update_purchase(data)
                return response, status

    @decorators.handle_exceptions
    def get(self, user_id=None):
        if user_id:
            response, status = authentication.authenticate(request.headers)
            if status != 200:
                return response, status

        response, status = get_purchases(user_id)
        return response, status

    @decorators.handle_exceptions
    def delete(self, user_id):
        response, status = delete_purchase(user_id)
        return response, status


class PurchaseDump(Resource):
    @decorators.handle_exceptions
    def get(self, user_id=None):
        response, status = purchase_dump(user_id)
        return response, status


class PurchaseValidation(Resource):
    @decorators.handle_exceptions
    def post(self):
        data = request.get_json()
        err = validators.validate_fields(data, 'cart')
        if err:
            err = f'Fields are missing: {", ".join(err)}'
            return err, 400
        else:
            response, status = purchase_validation(data)
            return response, status


# Purchase endpoints
api.add_resource(Purchase, '/api/purchase/',
                 endpoint="purchase",
                 methods=['POST', 'GET'])
api.add_resource(Purchase, '/api/purchase/',
                 endpoint="server_update_purchase",
                 methods=['PUT'])
api.add_resource(Purchase, '/api/purchase/<user_id>',
                 endpoint="user_update_purchase",
                 methods=['PUT'])
api.add_resource(Purchase, '/api/userpurchases/<user_id>',
                 endpoint="list_user_purchases",
                 methods=['GET', 'DELETE'])

# PurchaseDump endpoints
api.add_resource(PurchaseDump, '/api/purchasedump/',
                 endpoint="purchase_dump",
                 methods=['GET'])
api.add_resource(PurchaseDump, '/api/purchasedump/<user_id>',
                 endpoint="user_purchase_dump",
                 methods=['GET'])

# PurchaseValidation endpoints
api.add_resource(PurchaseValidation, '/api/purchasevalidation/',
                 endpoint="purchase_validation",
                 methods=['POST'])
