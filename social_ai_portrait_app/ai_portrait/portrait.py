import google.generativeai as genai

from settings.config import google_creds
from social_ai_portrait_app.ai_portrait.abstract import AbstractPortrait

gemini_api_key = google_creds.gemini_api_key


class Gemini(AbstractPortrait):
    def __init__(self):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.0-pro-latest",
            generation_config=genai.types.GenerationConfig(
                # Only one candidate for now.
                candidate_count=1,
                max_output_tokens=200,
                temperature=1.0)
        )

    async def get_text_portrait(self, input_: tuple | str) -> str:
        input_text = (f'Describe me in 10 sentences maximum! '
                      f'Please be creative! Do not forget to add a '
                      f'welcoming phrase! There is some information about me: '
                      f'I like YouTube videos about: {input_[0]}.'
                      f'I do not like YouTube videos about: {input_[1]}')
        response = await self.model.generate_content_async(input_text)
        return response.text


portrait = Gemini()
