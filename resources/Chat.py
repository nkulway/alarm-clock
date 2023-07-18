import openai
import os
from dotenv import load_dotenv
from resources.Weather import Weather
from elevenlabs import generate, play, set_api_key, clone

load_dotenv()
set_api_key(os.environ.get("ELEVEN_LABS_API_KEY"))
openai.api_key = os.environ.get("OPENAI_API_KEY")


class Chat:
    def getWeather():
        res = Weather.weather()
        print(res["weather"][0]["description"])
        weather = res["weather"][0]["description"]
        temp = res["main"]["temp"]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Give a wakeup greeting mentioning this value as the temperature {temp} and this weather description {weather} no longer than 30 words like a pirate.",
                }
            ],
        )
        return completion

    def getTextToSpeech():
        completion = Chat.getWeather()
        print(completion.choices[0].message.content)
        audio = generate(
            text=completion.choices[0].message.content,
            voice="Sam",
            model="eleven_monolingual_v1",
        )
        return audio
