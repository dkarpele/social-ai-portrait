from abc import ABC, abstractmethod


class AbstractPortrait(ABC):

    @abstractmethod
    async def get_text_portrait(self, input_: tuple | str) -> str:
        pass
