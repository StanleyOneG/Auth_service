import requests
import pytest
from contextlib import closing
from .settings import test_settings, conn
from functional.utils.endpoints import Endpoints

TEST_USER_EMAIL = 'testmail@test.com'
TEST_USER_PASSWORD = 'test'
TEST_USER_LOGIN = 'test_user'


pytest_plugins = [
    'auth_tests.functional.fixtures.fixture_requests'
]


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
