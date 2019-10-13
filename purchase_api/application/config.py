
import os

DB_NAME = os.environ.get("DB_NAME", "")
DB_URL = os.environ.get("DB_URL", "")

DB_TEST_NAME = os.environ.get("DB_TEST_NAME", "")
DB_TEST_URL = os.environ.get("DB_TEST_URL", "")


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SECRET_KEY = 'my_precious'  # new


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    MONGODB_SETTINGS = {
        'db': DB_NAME,
        'host': DB_URL
    }



class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGODB_SETTINGS = {
        'db': DB_TEST_NAME,
        'host': DB_TEST_URL
    }