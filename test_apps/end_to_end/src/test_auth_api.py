import unittest
from unittest.mock import patch, AsyncMock

import pytest
from httpx import AsyncClient

from auth_api.src.main import app
from auth_app.auth import create_signature
from test_apps.end_to_end.settings import settings


@pytest.mark.usefixtures('redis_clear_data_before_after',)
class TestOAuth(unittest.IsolatedAsyncioTestCase):
    @patch('auth_app.auth.Oauth2Manager.build_user_creds',
           new_callable=AsyncMock)
    @patch('helpers.utils.Bot.send_message',
           new_callable=AsyncMock)
    @pytest.mark.anyio
    async def test_callback_aiogoogle(self,
                                      mock_bot_send_message,
                                      mock_build_user_creds,
                                      ):
        signature = await create_signature('123456')
        code = 'good code'
        mock_build_user_creds.return_value = {
            'access_token': 'good access token', 'refresh_token': None,
            'expires_in': None, 'expires_at': None, 'scopes': None,
            'id_token': None, 'id_token_jwt': None, 'token_type': None,
            'token_uri': None, 'token_info_uri': None, 'revoke_uri': None}
        mock_bot_send_message.return_value = 'send message with bot'

        async with AsyncClient(app=app,
                         base_url=settings.auth_url) as ac:
            response = await ac.get(
                f"/callback/aiogoogle?"
                f"state={signature.decode()}&"
                f"code={code}&"
                f"scope=https://www.googleapis.com/auth/youtube.force-ssl")

        assert response.status_code == 307
        assert str(response.next_request.url) == settings.bot_url
        assert 1 == 0
