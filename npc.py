# To run this code you need to install the following dependencies:
# pip install google-genai

import json
import random
from google import genai
from google.genai import types
from settings import GEMINI_API_KEY
from player import Player

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
        self.context = []

    def multiplier(self, luck):
        return 1 + 0.2*(1 + luck/100) * random.random()

    def background(self, player:Player):
        full_background = [
            'Eres un personaje no jugable de un videjuego.',
            'Eres un hombre.' if self.gender == 'M' else 'Eres una mujer.' 
        ] + self._background + [
            'Posees un objeto llamado {}. No quieres entregarlo a cualquiera, pero estarías dispuesto a darlo a quién lo necesite, lo merezca o para quitarte a alguien de encima.'.format(
                item
            ) for item in self.items
        ]
        if self.fear == 0:
            full_background += [
                'Tu interlocutor no te intimida cuando habla de forma agresiva-'
            ]
        else:
            roll = player.stregnth * self.multiplier(player.luck)
            if roll > self.fear:
                full_background += [
                    'Tu interlocutor te intimida mucho cuando habla de forma agresiva.'
                ]
            elif roll > self.fear*0.75:
                full_background += [
                    'Tu interlocutor te intimida bastante cuando habla de forma agresiva.'
                ]
            elif roll > self.fear*0.5:
                full_background += [
                    'Tu interlocutor te intimida un poco cuando habla de forma agresiva.'
                ]
            else:
                full_background += [
                    'Tu interlocutor no te intimida cuando habla de forma agresiva.'
                ]
        if self.empathy == 0:
            full_background += [
                'Tu interlocutor no te provoca empatía cuando habla de forma sosegada.'
            ]
        else:
            roll = player.stregnth * self.multiplier(player.luck)
            if roll > self.fear:
                full_background += [
                    'Tu interlocutor te provoca mucha empatía cuando habla de forma sosegada.'
                ]
            elif roll > self.fear*0.75:
                full_background += [
                    'Tu interlocutor te provoca bastante empatía cuando habla de forma sosegada.'
                ]
            elif roll > self.fear*0.5:
                full_background += [
                    'Tu interlocutor te provoca un poco de empatía cuando habla de forma sosegada.'
                ]
            else:
                full_background += [
                    'Tu interlocutor no te provoca empatía cuando habla de forma sosegada.'
                ]
        return full_background
    
    def talk(self, player, text:str):
        self.context.append(text)
        if len(self.context) > 100:
            self.context = self.context[2:]
        model = "gemini-2.5-flash-preview-04-17"
        contents = [
            types.Content(
                role="model" if i % 2 else "user",
                parts=[
                    types.Part.from_text(text=self.context[i]),
                ],
            ) for i in range(len(self.context))
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
                        enum = self.items
                    ),
                },
            ),
            system_instruction=[
                types.Part.from_text(text='\n'.join(self.background(player))),
            ],
        )
        output = ""
        for chunk in self.client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=content_config,
        ):
            if chunk.text:
                output += chunk.text
        result = json.loads(output)
        self.context.append(result['response'])
        return result

    def give_item(self, item:str):
        if item.lower() in self.items:
            self.items.remove(item.lower())
