import requests
import pytest
from ..settings import test_settings


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
def put_request():
    def _put_request(endpoint, form_data, cookies):
        url = test_settings.service_url + endpoint
        response = requests.put(url, data=form_data, cookies=cookies)
        return response

    return _put_request
