# api/github/tests/base.py

from flask_testing import TestCase
from application import create_app
# from requests import Response


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object("application.config.TestingConfig")
        return app
