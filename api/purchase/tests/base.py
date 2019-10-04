# api/github/tests/base.py

from flask_testing import TestCase
from purchase import create_app
import os
from requests import Response


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.from_object("purchase.config.TestingConfig")
        return app
