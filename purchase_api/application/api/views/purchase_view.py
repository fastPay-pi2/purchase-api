from flask import Blueprint, request
from flask_restful import Resource, Api
from application.api.utils.db_utils import get_doc_by_attr, db_dump

from application.api.controllers.purchase_controller import save_purchase, update_purchase, post_purchase, start_purchase, get_all_purchases

from application.api.utils.validators import validate_rfid, validate_fields
from application.api.utils.handlers import handle_exceptions
from application.api.utils.data_formatter import format_message

from flask_cors import CORS


purchase_blueprint = Blueprint('views', __name__)
api = Api(purchase_blueprint)
CORS(purchase_blueprint)

class StartPurchase(Resource):
    def post(self):
        data = request.get_json()
        is_valid = validate_fields(data, 'user_id', 'cart_id')
        if is_valid:
            return start_purchase(data)
        else:
            return {'error': 'not ok'}

class Purchase(Resource):
    def post(self):
        data = request.get_json()
        err = validate_fields(data, 'user_id', 'cart_id')
        if err:
            err = f'Fields are missing: {", ".join(err)}'
            return format_message(err, 400)
        else:
            return start_purchase(data)

    def put(self, purchase_id):
        post_data = request.get_json()
        success_message = {
            "message": f"Purchase {purchase_id} successfully updated"
        }
        return handle_exceptions(update_purchase,
                                 success_message,
                                 post_data, purchase_id)

    def get(self):
        purchases = get_all_purchases()
        # db_json = db_dump()
        return purchases, 200
        
api.add_resource(StartPurchase, '/api/purchase/start/',
                 endpoint='start_purchase',
                 methods=['POST'])
api.add_resource(Purchase, '/api/purchase/',
                 endpoint="purchase",
                 methods=['POST', 'GET'])
api.add_resource(Purchase, '/api/purchase/<purchase_id>',
                 endpoint="update_purchase",
                 methods=['PUT'])
# api.add_resource(Purchase, '/api/purchase/',
#                  endpoint="all_purchases",
#                  methods=['GET'])
