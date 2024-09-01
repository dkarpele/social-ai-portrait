from abc import ABC, abstractmethod


class AbstractContent(ABC):
    """
    Abstract base class for fetching content information from social media platforms.

    This class defines an interface for retrieving specific data about a user's
    social media content that can be used for generating a social AI profile.
    Concrete implementations should inherit from this class and provide methods
    for:

    - Retrieving content details relevant to social AI profile generation.
    """
    @staticmethod
    @abstractmethod
    async def get_videos_tags(user_creds):
        """
        Asynchronously retrieves tags from the user's liked and disliked videos.

        This static method should retrieve tags associated with the user's most
        recent liked and disliked videos on a specific social media platform
        (e.g., YouTube). It should return a tuple containing two lists: one for
        tags from liked videos and one for tags from disliked videos.

        :param user_creds: User credentials required for accessing the social
        media platform's API.
        :return: A tuple containing two lists of tags (liked, disliked).
        """
        pass
