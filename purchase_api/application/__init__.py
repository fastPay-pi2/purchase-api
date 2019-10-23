from flask_cors import CORS
from flask import Flask
import os

cors = CORS()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    cors.init_app(app)
    # register blueprints
    from application.api.views.cart_view import cart_blueprint
    from application.api.views.purchase_view import purchase_blueprint
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(purchase_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app}  # tirei um 'db': db

    return app
