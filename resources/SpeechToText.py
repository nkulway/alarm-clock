import speech_recognition as sr


class SpeechToText:
    def speech_to_text():

        recognizer = sr.Recognizer()

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Speak something...")
            # Adjust for ambient noise for better recognition
            recognizer.adjust_for_ambient_noise(source)
            # Listen to the audio and attempt to recognize speech
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            # Use Google Web Speech API for speech recognition
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Error accessing Google Web Speech API: {e}")

    if __name__ == "__light_sensor__":
        speech_to_text()
