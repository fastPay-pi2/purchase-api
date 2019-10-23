
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from application import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('application.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['MONGODB_SETTINGS'] == {
                'db': os.environ.get('DB_NAME'),
                'host': os.environ.get('DB_URL')
            }
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('application.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['MONGODB_SETTINGS'] == {
                'db': os.environ.get('DB_TEST_NAME'),
                'host': os.environ.get('DB_TEST_URL')
            }
        )


if __name__ == '__main__':
    unittest.main()
