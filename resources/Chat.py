import openai
import os
from typing import TypedDict
from dotenv import load_dotenv
from resources.Weather import Weather
from elevenlabs import generate, play, set_api_key, clone

load_dotenv()
set_api_key(os.environ.get("ELEVEN_LABS_API_KEY"))
openai.api_key = os.environ.get("OPENAI_API_KEY")

class WeatherDetails(TypedDict):
    description: str
    currentTemp: str

class Chat:
    def get_greeting_with_weather() -> str:
        res = Weather.weather()
        print(res["weather"][0]["description"])
        weather = res["weather"][0]["description"]
        temp = res["main"]["temp"]
        greeting  = f"Give a wakeup greeting mentioning this value as the temperature {temp} and this weather description {weather}"
        return greeting
    
    def get_greeting(text: str):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"{text} no longer than 30 words like a pirate.",
                }
            ],
        )
        return completion

    def get_text_to_speech(text: str):
        completion = Chat.get_greeting(text)
        print(completion.choices[0].message.content)
        audio = generate(
            text=completion.choices[0].message.content,
            voice="Sam",
            model="eleven_monolingual_v1",
        )
        return audio