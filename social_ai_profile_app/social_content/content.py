import asyncio
import logging

from aiogoogle import Aiogoogle

from project_settings.config import client_creds
from social_ai_profile_app.social_content.abstract import AbstractContent

logger = logging.getLogger(__name__)


class YouTubeContent(AbstractContent):
    """
    Implementation of `AbstractContent` for fetching video tags from YouTube.

    This class utilizes the Aiogoogle library to access YouTube's API and
    retrieve tags associated with the user's liked and disliked videos.
    It follows the interface defined in `AbstractContent` for fetching video tags.
    """
    @staticmethod
    async def get_videos_tags(user_creds) -> tuple[list, list]:
        """
        Retrieves tags from the user's liked and disliked videos on YouTube.

        This method asynchronously fetches tags from the user's most recent 5
        liked and disliked videos on YouTube using the provided user credentials.
        It utilizes Aiogoogle to interact with YouTube's API and returns a tuple
        containing two lists: one for tags from liked videos and one for tags
        from disliked videos.

        :param user_creds: User credentials required for accessing YouTube's API.
        :return: A tuple containing two lists of tags (liked, disliked).
        """
        logger.debug('Getting tags for the resent 5 liked and disliked videos')
        async with Aiogoogle(user_creds=user_creds,
                             client_creds=client_creds) as aiogoogle:
            youtube_v3 = await aiogoogle.discover('youtube', 'v3')
            liked_videos_coro = aiogoogle.as_user(
                youtube_v3.videos.list(
                    part="snippet",
                    myRating="like",
                    maxResults=5,
                )
            )
            disliked_videos_coro = aiogoogle.as_user(
                youtube_v3.videos.list(
                    part="snippet",
                    myRating="dislike",
                    maxResults=5,
                )
            )
            liked_videos, disliked_videos = await asyncio.gather(
                liked_videos_coro,
                disliked_videos_coro)

        def create_tags_list(videos: dict) -> list:
            """
            Generates a list of tags from a dictionary of videos, taking only
            the first 5 tags from each video.

            :param videos (dict): A dictionary containing information about videos.
            :return list: A list of tags.
            """
            for item in videos['items']:
                try:
                    tags = item['snippet']['tags']
                    yield from tags[:5]
                except KeyError:
                    logger.info(f'Video "{item["snippet"]["title"]}" has no tags.')

        tags_liked_videos: list = list(create_tags_list(liked_videos))
        tags_disliked_videos: list = list(create_tags_list(disliked_videos))
        return tags_liked_videos, tags_disliked_videos


content = YouTubeContent()
