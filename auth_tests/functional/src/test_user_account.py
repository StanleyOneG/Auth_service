from contextlib import closing
import datetime
from http import HTTPStatus
import pytest
from functional.settings import conn
from requests import Response
from functional.conftest import (
    TEST_USER_EMAIL,
    TEST_USER_LOGIN,
    TEST_USER_PASSWORD,
)


def test_user_sugn_up(post_request):
    """Should create a new user."""
    response = post_request(
        '/api/v1/user/register',
        {
            'login': TEST_USER_LOGIN,
            'password': TEST_USER_PASSWORD,
            'email': TEST_USER_EMAIL,
        },
    )
    with closing(conn.cursor()) as cursor:
        cursor.execute("SELECT * FROM auth.user")
        user = cursor.fetchall()[-1]  # get last user

    assert response.status_code == HTTPStatus.OK
    assert user[1] == TEST_USER_LOGIN  # get user login
    assert user[2] == TEST_USER_EMAIL  # get user email


def improper_user_sugn_up(post_request):
    """Should not create a new user."""
    response = post_request(
        '/api/v1/user/register',
        {
            'login': TEST_USER_LOGIN,
            'password': TEST_USER_PASSWORD,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        (TEST_USER_EMAIL, TEST_USER_PASSWORD, HTTPStatus.OK),
        ('bad_email@test.com', 'test', HTTPStatus.UNAUTHORIZED),
    ],
)
def test_user_login(post_request, email, password, status_code):
    """Should login user."""
    response = post_request(
        '/api/v1/user/login',
        {'email': email, 'password': password},
    )
    assert response.status_code == status_code


def test_user_log_history(post_request, get_request):
    """Should get user log history."""
    login_response: Response = post_request(
        '/api/v1/user/login',
        {
            'email': TEST_USER_EMAIL,
            'password': TEST_USER_PASSWORD,
        },
    )
    login_time = datetime.datetime.now()
    hist_response: Response = get_request(
        '/api/v1/user/show_login_history',
        cookies=login_response.cookies,
    )
    result = hist_response.json()
    assert hist_response.status_code == HTTPStatus.OK
    assert result[0]['login_time'] == login_time.strftime(
        '%Y-%m-%d %H:%M:%S',
    )


def test_user_change_credentials(post_request, put_request):
    """Should change user credentials."""
    initial_login_response: Response = post_request(
        '/api/v1/user/login',
        {
            'email': TEST_USER_EMAIL,
            'password': TEST_USER_PASSWORD,
        },
    )
    cookies = initial_login_response.cookies
    change_response: Response = put_request(
        '/api/v1/user/change_credentials',
        {'login': 'new_login'},
        cookies=cookies,
    )
    with closing(conn.cursor()) as cursor:
        cursor.execute("SELECT * FROM auth.user")
        user = cursor.fetchall()[-1]  # get last user

    assert change_response.status_code == HTTPStatus.OK
    assert user[1] == 'new_login'  # get user login


def test_user_logout(do_test_user_login, patch_request):
    """Should logout user."""
    response: Response = do_test_user_login()
    cookies = response.cookies
    logout_response: Response = patch_request(
        '/api/v1/user/logout',
        cookies=cookies,
    )
    assert response.status_code == HTTPStatus.OK
    assert len(logout_response.cookies) == 0


def test_refresh_jwt_tokens(do_test_user_login, delete_request):
    """Should refresh jwt tokens."""
    response: Response = do_test_user_login()
    cookies = response.cookies
    refresh_response: Response = delete_request(
        '/api/v1/user/refresh',
        cookies=cookies,
    )
    assert response.status_code == HTTPStatus.OK
    assert refresh_response.cookies != cookies
