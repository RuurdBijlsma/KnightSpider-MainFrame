import os
import random

import time
from pygame import mixer
from gtts import gTTS

SENTENCES = [
    "Beep beep lettuce",
    "speedtest is lies",
    "fast.com is good shit right there"
]

FILE_NAME = "temp.mp3"

mixer.init()

def speak_random():
    speak(random.choice(SENTENCES))

def speak(text):
    print("saying", text)
    # os.system("espeak -s 125 -v en+m3 '{}'".format(text))
    tts = gTTS(text, lang="en")
    tts.speed = 10
    tts.save(FILE_NAME)
    mixer.music.load(FILE_NAME)
    mixer.music.play()


def main():
    speak_random()
    time.sleep(10)

if __name__ == '__main__':
    main()
