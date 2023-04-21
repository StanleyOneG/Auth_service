import os
from datetime import timedelta

from .config import (
    DB_URI,
    REDIS_ACCESS_TOKEN_EXPIRE,
    REDIS_REFRESH_TOKEN_EXPIRE
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend(),
)

public_key = private_key.public_key()


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
