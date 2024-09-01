from abc import ABC, abstractmethod


class AbstractPortrait(ABC):
    """
    Abstract base class for AI-powered text profile generation.

    This class defines the core functionality for generating a textual description
    of a user based on some input data. Concrete implementations should
    inherit from this class and provide an implementation for:

    - Retrieving a textual social AI profile for the user.
    """
    @abstractmethod
    async def get_text_profile(self, input_: tuple | str) -> str:
        """
        Asynchronously retrieves a text profile description for the user.

        This method takes an input (either a tuple or a string) specific to the
        chosen AI model and returns a textual description generated based on
        that input.

        :param input_: The input data for the AI model (format depends on the model).
        :return: The generated textual social AI profile for the user.
        """
        pass
