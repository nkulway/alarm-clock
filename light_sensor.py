import time
import RPi.GPIO as GPIO
from elevenlabs import play
from resources.Chat import Chat
from resources.SpeechToText import SpeechToText


class AlarmClock:
    def alarm_clock():
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
                isNight = False
                print("TIME TO WAKE UP")
                
                greeting = Chat.get_greeting_with_weather()
                greeting_audio = Chat.get_text_to_speech(greeting)
                play(greeting_audio)
                
                user_response = SpeechToText.speech_to_text()
                chat_response = Chat.get_text_to_speech(user_response)
                play(chat_response)

            time.sleep(1)


    if __name__ == "__main__":
        alarm_clock()



# To be used with paid tier

# voice = clone(
#     name="Gandalf",
#     description="A wizard who proves himself to possess the leadership traits of Impartiality, experience, kindness and affection for all others, he commands respect, he is wise and thoughtful and he understands the need for sacrifice to achieve the ultimate victory for Middle Earth.",
#     files=["./samples/1a-a-wizard-is-never-late.mp3", "./samples/1c-im-trying-to-help-you.mp3"]
# )
