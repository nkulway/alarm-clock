import os
import sys
import openai
import RPi.GPIO as GPIO
import time
from elevenlabs import generate, play, set_api_key, clone
from dotenv import load_dotenv
from weather import weather

load_dotenv()
set_api_key(os.environ.get("ELEVEN_LABS_API_KEY"))
openai.api_key = os.environ.get("OPENAI_API_KEY")

GPIO.setmode(GPIO.BOARD)

resistorPin = 7
isNight = True
while isNight:
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()
    diff = 0

    while GPIO.input(resistorPin) == GPIO.LOW:
        diff = time.time() - currentTime

    sensorReading = diff * 1000

    print(sensorReading)

    if sensorReading > 30:
        # do nothing
        print("LIGHTS OFF")
    elif sensorReading < 30:
        # trigger generative ai voice
        print("TIME TO WAKE UP")
        res = weather()
        print(res["weather"][0]["description"])
        weather = res["weather"][0]["description"]
        temp = res['main']['temp']
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Give a wakeup greeting mentioning this value as the temperature {temp} and this weather description {weather} no longer than 30 words like a pirate.",
                }
            ],
        )

        audio = generate(
            text=completion.choices[0].message.content,
            voice="Sam",
            model="eleven_monolingual_v1",
        )

        print(completion.choices[0].message.content)

        play(audio)
        print(sys.path)
        isNight = False

    time.sleep(1)


# To be used with paid tier

# voice = clone(
#     name="Gandalf",
#     description="A wizard who proves himself to possess the leadership traits of Impartiality, experience, kindness and affection for all others, he commands respect, he is wise and thoughtful and he understands the need for sacrifice to achieve the ultimate victory for Middle Earth.",
#     files=["./samples/1a-a-wizard-is-never-late.mp3", "./samples/1c-im-trying-to-help-you.mp3"]
# )
