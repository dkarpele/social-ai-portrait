import json
import logging
from aiofiles import os, open
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import UserCreds
from aiogoogle.auth.managers import Oauth2Manager
from aiogoogle.excs import AuthError, HTTPError
from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from telegram import Bot

from settings.config import google_client_creds, bot_settings

router = APIRouter()


@router.get('/callback/aiogoogle',
            # response_model=Token,
            status_code=status.HTTP_200_OK,
            description="Redirect URI, указанный при регистрации приложения.",
            response_description="code: Код подтверждения возвращается в URL"
                                 " перенаправления.",
            include_in_schema=False
            )
async def callback(code: int | str,
                   state: str):
    """Calls the Apps Script API."""

    user_creds: UserCreds | None = None
    oauth2manager = Oauth2Manager()
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if await os.path.exists("token.json"):
        async with open("token.json", 'r') as token_file:
            contents = await token_file.read()
            user_creds = UserCreds(**json.loads(contents))

    # If the access token available, let the user log in.
    if not user_creds or oauth2manager.is_expired(user_creds):
        if user_creds and user_creds.refresh_token:
            try:
                _, user_creds = await oauth2manager.refresh(
                    user_creds=user_creds,
                    client_creds=google_client_creds)
            # if refresh token has expired create new user creds.
            except (AuthError, HTTPError) as ae:
                logging.warning('Refresh token has expired, creating new '
                                'user credentials')
                user_creds = UserCreds(**await oauth2manager.build_user_creds(
                    grant=code,
                    client_creds=google_client_creds
                ))
        else:
            user_creds = UserCreds(**await oauth2manager.build_user_creds(
                grant=code,
                client_creds=google_client_creds

            ))
        # Save the credentials for the next run
        async with open("token.json", "w") as token_file:
            await token_file.write(json.dumps(user_creds))

    # Here, you should store full_user_creds in a db. Especially the refresh
    # token and access token.
    print(user_creds)
    async with Aiogoogle(user_creds=user_creds,
                         client_creds=google_client_creds) as aiogoogle:
        youtube_v3 = await aiogoogle.discover('youtube', 'v3')
        result = await aiogoogle.as_user(
            youtube_v3.videos.list(
                part="snippet,contentDetails,statistics",
                myRating="like",
            )
        )
    print(result)
    state_obj = json.loads(state)
    chat_id = state_obj['chat_id']
    bot = Bot(bot_settings.token)
    async with bot:
        await bot.send_message(text='Auth was successful!', chat_id=chat_id)
    return RedirectResponse(url='https://t.me/SocialAIPortraitBot')
