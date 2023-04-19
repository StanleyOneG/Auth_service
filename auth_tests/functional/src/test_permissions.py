from http import HTTPStatus

import pytest

from functional.utils.endpoints import Endpoints
from functional.conftest import (
    TEST_USER_EMAIL,
    TEST_USER_LOGIN,
    TEST_USER_PASSWORD
)


def test_create(post_request):
    """Nonprivileged user creates permission"""
    data = {
        'email': TEST_USER_EMAIL,
        'login': TEST_USER_LOGIN,
        'password': TEST_USER_PASSWORD
    }
    result = post_request(Endpoints.UserSignUp.value,
                 data=data)
    cookies = result.cookies

    data = {
        'permission': 'test_permission'
    }
    result = post_request(Endpoints.CreatePermission.value,
                          data=data,
                          cookies=cookies)
    assert result.status_code == HTTPStatus.FORBIDDEN
    
    
def test_delete(delete_request, do_test_user_login):
    """Nonprivileged user deletes permission"""
    result = do_test_user_login()
    cookies = result.cookies
    data = {
        'permission': 'test_permission'
    }
    result = delete_request(Endpoints.DeletePermission.value,
                            data=data,
                            cookies=cookies)
    assert result.status_code == HTTPStatus.FORBIDDEN


def test_set_to_user(post_request, do_test_user_login):
    """Nonprivileged user sets permission to another user"""
    result = do_test_user_login()
    cookies = result.cookies
    data = {
        'permission': 'dummy',
        'user_login': TEST_USER_LOGIN
    }
    result = post_request(Endpoints.SetUserPermission.value,
                          data=data,
                          cookies=cookies)
    assert result.status_code == HTTPStatus.FORBIDDEN


def test_change(patch_request, do_test_user_login):
    """Nonprivileged user changes permission"""
    result = do_test_user_login()
    cookies = result.cookies
    data = {
        'old_permission': 'dummy',
        'new_permission': 'more_dummy'
    }
    result = patch_request(Endpoints.ChangePermission.value,
                           data=data,
                           cookies=cookies)
    assert result.status_code == HTTPStatus.FORBIDDEN


def test_show_my(get_request, do_test_user_login):
    """Nonprivileged user gets list permission"""
    result = do_test_user_login()
    cookies = result.cookies
    data = {
        'user_login': TEST_USER_LOGIN,
    }
    result = get_request(Endpoints.ShowUserPermissions.value,
                         data=data,
                         cookies=cookies)
    assert result.status_code == HTTPStatus.FORBIDDEN


def test_show_all(get_request, do_test_user_login):
    """Nonprivileged user gets list permission"""
    result = do_test_user_login()
    cookies = result.cookies
    result = get_request(endpoint=Endpoints.ShowPermissions.value,
                         cookies=cookies)
    assert result.status_code == HTTPStatus.FORBIDDEN


def test_delete_to_user(delete_request, do_test_user_login):
    """Nonprivileged user deletes permission to another"""
    result = do_test_user_login()
    cookies = result.cookies
    data = {
        'permission': 'more_dummy',
        'user_login': TEST_USER_LOGIN
    }
    result = delete_request(endpoint=Endpoints.DeleteUserPermission.value,
                            data=data,
                            cookies=cookies)
    assert result.status_code == HTTPStatus.FORBIDDEN
