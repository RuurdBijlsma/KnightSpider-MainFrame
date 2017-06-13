import subprocess
import random

import time
from pygame import mixer
from gtts import gTTS

import pyttsx

SENTENCES = [
    "Beep beep lettuce",
    "speedtest is lies",
    "fast.com is good shit right there"
]

FILE_NAME = "temp.mp3"

# mixer.init()
tts_engine = pyttsx.init()
tts_engine.setProperty('rate', 100)


def speak_random():
    speak(random.choice(SENTENCES))

def speak(text):
    print("saying", text)
    tts_engine.setProperty("voice", b'punjabi')
    tts_engine.say(text)
    # subprocess.call(["espeak", text])
    # tts = gTTS(text, lang="en-uk")
    # tts.speed = 10
    # tts.save(FILE_NAME)
    # mixer.music.load(FILE_NAME)
    # mixer.music.play()


def main():
    # speak_random()
    for voice in tts_engine.getProperty('voices'):
        print(voice.id)
        tts_engine.setProperty("voice", voice.id)
        tts_engine.say("test")

    tts_engine.runAndWait()

if __name__ == '__main__':
    main()
