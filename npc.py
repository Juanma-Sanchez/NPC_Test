# To run this code you need to install the following dependencies:
# pip install google-genai

import json
from google import genai
from google.genai import types
from settings import GEMINI_API_KEY

class NPC:
    def __init__(self, name:str, gender:str, background:list, items:list, fear:int, empathy:int):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=types.HttpOptions(api_version='v1alpha')
        )
        self.name = name
        self.gender = gender
        self._background = background
        self.items = items
        self.fear = fear
        self.empathy = empathy

    def background(self):
        full_background = [
            'Eres un personaje no jugable de un videjuego.',
            'Eres un hombre.' if self.gender == 'M' else 'Eres una mujer.' 
        ] + self._background + [
            'Posees un objeto llamado {}. Estás dispuesto a entregarlo a quién lo necesite, lo merezca o para quitarte a alguien de encima.'.format(
                item
            ) for item in self.items
        ]
        # TODO add fear and empathy background
        return full_background
    
    def talk(self, player, text:str):
        model = "gemini-2.5-flash-preview-04-17"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=text),
                ],
            ),
        ]
        content_config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type = genai.types.Type.OBJECT,
                required = ["response", "keep_talking"],
                properties = {
                    "response": genai.types.Schema(
                        type = genai.types.Type.STRING,
                    ),
                    "keep_talking": genai.types.Schema(
                        type = genai.types.Type.BOOLEAN,
                    ),
                    "item": genai.types.Schema(
                        type = genai.types.Type.STRING,
                    ),
                },
            ),
            system_instruction=[
                types.Part.from_text(text='\n'.join(self.background())),
            ],
        )
        output = ""
        for chunk in self.client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=content_config,
        ):
            output += chunk.text
        return json.loads(output)

