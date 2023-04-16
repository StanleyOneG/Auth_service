from http import HTTPStatus
import logging
import pytest
from ..settings import test_settings

pytestmarkasync = pytest.mark.asyncio

logger = logging.getLogger('tests')

@pytestmarkasync
async def test_create(get_client_session):
    url = test_settings.service_url + "/api/v1/create_permission"
    query_params = {
        "permission": "test_permission",
    }
    async for session in get_client_session:
        response = await session.get(url, params=query_params)
    status = response.status
    json_response = await response.json()
    assert status == HTTPStatus.OK
