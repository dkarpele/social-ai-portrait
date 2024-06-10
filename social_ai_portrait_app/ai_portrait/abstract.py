from abc import ABC, abstractmethod


class AbstractPortrait(ABC):

    @abstractmethod
    async def get_text_profile(self, input_: tuple | str) -> str:
        pass
