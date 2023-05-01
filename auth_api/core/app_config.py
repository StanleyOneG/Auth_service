import os
from datetime import timedelta
from flask import current_app as app, request

from core.config import (
    DB_URI,
    REDIS_ACCESS_TOKEN_EXPIRE,
    REDIS_REFRESH_TOKEN_EXPIRE,
    JWT_PRIVATE_KEY,
    JWT_PUBLIC_KEY,
)

private_key = JWT_PRIVATE_KEY
public_key = JWT_PUBLIC_KEY


class Config(object):
    TESTING = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = DB_URI
    JWT_TOKEN_LOCATION = [
        "cookies",
    ]
    SECRET_KEY = os.urandom(32)
    JWT_ALGORITHM = "RS256"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=float(REDIS_ACCESS_TOKEN_EXPIRE / 60)
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        hours=float(REDIS_REFRESH_TOKEN_EXPIRE / 60 / 60)
    )
    JWT_PUBLIC_KEY = public_key
    JWT_PRIVATE_KEY = private_key
    # Disabled for development purposes. Turn on in Production
    JWT_COOKIE_CSRF_PROTECT = True
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = DB_URI
    JWT_TOKEN_LOCATION = [
        "cookies",
    ]
    SECRET_KEY = os.urandom(32)
    JWT_ALGORITHM = "RS256"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=float(REDIS_ACCESS_TOKEN_EXPIRE / 60)
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        hours=float(REDIS_REFRESH_TOKEN_EXPIRE / 60 / 60)
    )
    JWT_PUBLIC_KEY = public_key
    JWT_PRIVATE_KEY = private_key
    # Disabled for development purposes. Turn on in Production
    JWT_COOKIE_CSRF_PROTECT = False
    PROPAGATE_EXCEPTIONS = True
