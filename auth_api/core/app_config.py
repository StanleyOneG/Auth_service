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


# private_key = """
# -----BEGIN PRIVATE KEY-----
# MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCWtNxdEIXjMXZp
# YlR8MhFukbcLztdGC3/IhW8s1/wQIxQtz+jCPF9CFzt3UYNr0Zpv5PUJSS3o01fp
# BbQ275wNug2QdLh/lBJFehGmT8n/xVCk46XUoIp6Jhg30ofC79XHiXl9+iKkddmp
# 3ylmLp3Z5ipAm+9nq6f/V0R9x28bStMhzwz7t4uX7HDOErlFYbldP0kSuWvj4QfN
# kwvWfc+z2sFlBlZ1ztKys7MBFgZwXmj6ZVlxIi6wudZkLI8X2eF0BrRgq74D5nEx
# wpG47VQRIqG1FJjfF+gsyYVfPT+iSHvD4M7Qq6Y5emgWhdRX2ndvv4i23/ZVodhb
# +zP0IHB9AgMBAAECggEAAM+DOerrVXAAK4vwWWSpjFczTVh09vb73ne9Q9f7jpip
# tJ9gKJ9Lgd7/HmKtWsibVIu+N6kRmqV8XQ//SqZaSAaeqQ6/qUwCFyaTbroSI5KL
# nv9sdmrQo9yNl8tFmKpSk4qtQRy1z/2kSJIfNmH8zl27D3LnRD77ndd50lVexx5L
# SrqIIF/r2SpefqV0Ov1B6e0HrY/u4Tmawf29+aFjqjL5YQbRRMgcuMAGwyJIacDu
# Eb3NUK+Rp78l+IvNQr8q8R95YMSmnH3s6x5cPg8z4dg8hDW1Qw/eXHy5uSDmlQc4
# dEx4AhdrhQaKs4OI6mfEf1VVEmVmbY9OkjTyoy0JwQKBgQDU+7xJjXUDwrDixsQa
# rIWL87nCA8QSiLBDBmmi0iPaA2fUc7TZ6ueezL0I5h3GXTmXzg5QceueOH0/7Wnj
# T6/B32aJW90UMyjyQ2ryBy95BVkmEycs/8b79HVfCFGTU6fO0u4PD80fY0G4qDvs
# 4N5Cso4V6+4r2TvrqAjWFOTS3QKBgQC1JRysQkmhjS1G2IB04SE9npP6GcV1kJSj
# qhy5uOu4QfWXm9ega2Xt6oEBI0nrE/vpva6Bj9G7c6ijwhdrHHXg6agn8BamFJ34
# LmmEhMEqiPo98Oy3NI37k2ix4kTZBcihq6XoYQ69tSIB0Zy/M6zA1I5546g0i9d8
# fRoPWR0qIQKBgGmaVBaoM//kVe5rnaqYJjNpao5/bYW/Dp59HH2l8i7UB3R41pBC
# gAvl+kjiSJsleDwD6GcMxUYTPk8nOZyC02OukFnFGc49O607rlhJJcm81CIj1wXh
# 4NjmshenuULydL8BKRaAwDUy8tBLYkMmkC3D+N13uQU21hYXoCH+BCNlAoGAXbjZ
# 4PZbCk71Aha6P77LaApIHbp/w5gOj69QNXdL3oWh/9MN+V4X2sTeAiyz7gDk8cbG
# Jxq2NPpeYnvlifGru7ao3iEGVt+L7AB3b60QFGXSs4GXuCJk46kdHgwn+vFXIO6i
# ZFzzN4wkEDTXmMWvuAVBwibbvHQuBabkeNRuloECgYEAs+Snww0Bb8yhZxolNmeI
# rTWtHwtt5hyQucUrczoaVID4WT7lQUlnnK1onLGqu/NY643HvV74TAzM8IfjN9Ks
# hxtUAl0Rvuf8i/zhP00pZtt9knd/Vt5MFBzX3+YvhFfpJCwTh9MFjwWSP6g5Q+z0
# CdVXUMISAY78NlZpIo+fbXU=
# -----END PRIVATE KEY-----
# """
# public_key = """
# -----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlrTcXRCF4zF2aWJUfDIR
# bpG3C87XRgt/yIVvLNf8ECMULc/owjxfQhc7d1GDa9Gab+T1CUkt6NNX6QW0Nu+c
# DboNkHS4f5QSRXoRpk/J/8VQpOOl1KCKeiYYN9KHwu/Vx4l5ffoipHXZqd8pZi6d
# 2eYqQJvvZ6un/1dEfcdvG0rTIc8M+7eLl+xwzhK5RWG5XT9JErlr4+EHzZML1n3P
# s9rBZQZWdc7SsrOzARYGcF5o+mVZcSIusLnWZCyPF9nhdAa0YKu+A+ZxMcKRuO1U
# ESKhtRSY3xfoLMmFXz0/okh7w+DO0KumOXpoFoXUV9p3b7+Itt/2VaHYW/sz9CBw
# fQIDAQAB
# -----END PUBLIC KEY-----
# """


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
