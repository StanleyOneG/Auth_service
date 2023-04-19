import requests
import pytest
from contextlib import closing
from .settings import test_settings, conn
from functional.utils.endpoints import Endpoints

TEST_USER_EMAIL = 'testmail@test.com'
TEST_USER_PASSWORD = 'test'
TEST_USER_LOGIN = 'test_user'


@pytest.fixture
def post_request():
    def _post_request(endpoint, data=None, cookies=None):
        url = test_settings.service_url + endpoint
        response = requests.post(url, data=data, cookies=cookies)
        return response

    return _post_request


@pytest.fixture
def get_request():
    def _get_request(endpoint, data=None, cookies=None):
        url = test_settings.service_url + endpoint
        response = requests.get(url, data=data, cookies=cookies)
        return response

    return _get_request


@pytest.fixture
def patch_request():
    def _patch_request(endpoint, data=None, cookies=None):
        url = test_settings.service_url + endpoint
        response = requests.patch(url, data=data, cookies=cookies)
        return response

    return _patch_request


@pytest.fixture
def delete_request():
    def _delete_request(endpoint, data=None, cookies=None):
        url = test_settings.service_url + endpoint
        response = requests.delete(url, data=data, cookies=cookies)
        return response

    return _delete_request


@pytest.fixture
def do_test_user_login(post_request):
    def _do_test_user_login():
        data = {
                'email': TEST_USER_EMAIL,
                'password': TEST_USER_PASSWORD,
            }
        response = post_request(
            Endpoints.UserLogIn.value,
            data,
        )
        return response

    return _do_test_user_login


@pytest.fixture(scope='module', autouse=True)
def cleanup(request):
    """Truncate cascade the auth.user table after tests per module."""

    def _cleanup():
        with closing(conn.cursor()) as cursor:
            cursor.execute('TRUNCATE TABLE auth.user CASCADE')

    request.addfinalizer(_cleanup)
