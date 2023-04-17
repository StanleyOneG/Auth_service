import logging
from typing import Generator
import uuid
import pytest
import aiohttp
from redis import Redis
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from auth_tests.settings import test_settings
from auth_api.models.db_models import User

logger = logging.getLogger('tests')


@pytest.fixture(scope='function')
async def get_client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture(scope='module')
async def registered_user_access_token(get_client_session):
    """Fixture to register dummy user"""
    register_url = test_settings.service_url + "/api/v1/register"
    query_params = {
        "email": "test_permissions@test.com",
        "login": "test_permissions",
        "password": "test_permissions",
    }
    async for session in get_client_session:
        await session.get(register_url, params=query_params)
        cookies = session.cookie_jar.filter_cookies("access_token")
        return cookies["access_token"].value
