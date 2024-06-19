from abc import ABC, abstractmethod


class AbstractContent(ABC):
    @staticmethod
    @abstractmethod
    async def get_videos_tags(user_creds):
        pass
