# api/github/config.py
import os
from pymongo import MongoClient

DB_NAME = os.environ.get("DB_NAME", "")
DB_URL = os.environ.get("DB_URL", "")


class DevelopmentConfig():
    """Development configuration"""
    MONGO_DATABASE_URI = os.environ.get("DB_URL")


class TestingConfig():
    """Testing configuration"""
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGO_DATABASE_URI = os.environ.get("DB_TEST_URL")

