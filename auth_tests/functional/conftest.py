import requests
import json
import pytest
from functional.settings import test_settings, conn
import psycopg2
from contextlib import closing

TEST_USER_EMAIL = 'testmail@test.com'
TEST_USER_PASSWORD = 'test'
TEST_USER_LOGIN = 'test_user'


@pytest.fixture(scope='module', autouse=True)
def cleanup(request):
    """Truncate cascade the auth.user table after tests per module."""

    def _cleanup():
        with closing(conn.cursor()) as cursor:
            cursor.execute('TRUNCATE TABLE auth.user CASCADE')

    request.addfinalizer(_cleanup)


@pytest.fixture
def post_request():
    def _post_request(endpoint, form_data):
        url = test_settings.service_url + endpoint
        response = requests.post(url, data=form_data)
        return response

    return _post_request


@pytest.fixture
def get_request():
    def _get_request(endpoint, cookies=None):
        url = test_settings.service_url + endpoint
        response = requests.get(url, cookies=cookies)
        return response

    return _get_request


@pytest.fixture
def put_request():
    def _put_request(endpoint, form_data, cookies):
        url = test_settings.service_url + endpoint
        response = requests.put(url, data=form_data, cookies=cookies)
        return response

    return _put_request


@pytest.fixture
def patch_request():
    def _patch_request(endpoint, cookies):
        url = test_settings.service_url + endpoint
        response = requests.patch(url, cookies=cookies)
        return response

    return _patch_request


@pytest.fixture
def delete_request():
    def _delete_request(endpoint, cookies):
        url = test_settings.service_url + endpoint
        response = requests.delete(url, cookies=cookies)
        return response

    return _delete_request


@pytest.fixture
def testing_user_login(post_request):
    """Login a testing user."""

    def _testing_user_login():
        response = post_request(
            '/api/v1/user/login',
            {
                'email': TEST_USER_EMAIL,
                'password': TEST_USER_PASSWORD,
            },
        )
        return response

    return _testing_user_login
