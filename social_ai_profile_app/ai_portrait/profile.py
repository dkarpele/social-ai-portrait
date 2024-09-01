"""
This module provides a concrete implementation (`Gemini`) of the `AbstractPortrait` class
using Google's Generative AI (GenAI) API and the Gemini-1.5-flash model.

It generates a textual social AI profile description for the user based on their
preferences for YouTube videos (liked and disliked categories).
"""

import logging

import google.generativeai as genai

from project_settings.config import google_creds
from social_ai_profile_app.ai_portrait.abstract import AbstractPortrait

gemini_api_key = google_creds.gemini_api_key
logger = logging.getLogger(__name__)


class Gemini(AbstractPortrait):
    """
    Implementation of `AbstractPortrait` using Google's GenAI API and Gemini-1.5-flash model.

    This class configures the GenAI API with the provided API key and sets up
    the Gemini-1.5-flash model for text generation. It retrieves a textual profile
    description for the user based on their YouTube video preferences.
    """
    def __init__(self):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.types.GenerationConfig(
                # Only one candidate for now.
                candidate_count=1,
                max_output_tokens=200,
                temperature=1.0)
        )

    async def get_text_profile(self, input_: tuple | str) -> str:
        """
        Retrieves a textual social AI profile for the user using the Gemini model.

        This method takes a tuple containing the user's preferred (liked) and
        disliked YouTube video categories as input. It constructs a prompt
        including a welcoming phrase and information about the user's preferences.
        Finally, it uses the Gemini model to generate a textual social AI profile
        description based on the constructed prompt.

        :param input_: A tuple containing the user's liked and disliked YouTube
         video categories (str).
        :return: The generated textual social AI profile description for the user.
        """
        logger.debug('Getting user TEXT social AI profile with Gemini model.')
        input_text = (f'Describe me in 10 sentences maximum! '
                      f'Please be creative! Do not forget to add a '
                      f'welcoming phrase! There is some information about me: '
                      f'I like YouTube videos about: {input_[0]}. '
                      f'I do not like YouTube videos about: {input_[1]}')
        response = await self.model.generate_content_async(input_text)
        return response.text


profile = Gemini()
