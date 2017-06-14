import socket
import subprocess
import random

import time

import os

class SpeechSynthesis(object):
    SENTENCES = [
        "Beep beep lettuce",
        "hello i am kitt",
        "vroom vroom am car",
        "starting all systems"
    ]

    PROCESS_COMMAND = "festival"

    def __init__(self):
        try:
            ps = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
            festival = subprocess.Popen(["grep", self.PROCESS_COMMAND], stdin=ps.stdout, stdout=subprocess.PIPE)
            clean = subprocess.check_output(["grep", "-v", "grep"], stdin=festival.stdout)

            lines = len(clean.decode().split('\n')) - 1
            # print(clean.decode())
            print("instances", lines)

            if lines == 1:
                self.connect_server()
                return

            if lines > 1:
                print("Too many instances, cleaning up")
                os.system("killall festival")
                self.start_server()

        except subprocess.CalledProcessError as e:
            self.start_server()
            print(e)


    def start_server(self):
        print("Spawning server")
        subprocess.Popen(["festival", "--server"], stdout=subprocess.PIPE)
        time.sleep(0.1)
        return self.connect_server()

    def connect_server(self):
        t_start = time.time()
        while t_start + 5 > time.time():
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(("127.0.0.1", 1314))
                return True
            except:
                time.sleep(0.1)

        print("Failed to connect")
        return False



    def speak_random(self):
        self.speak(random.choice(self.SENTENCES))

    def speak(self, text):
        print("saying", text)
        self.socket.send("(SayText '\"{}\")".format(text + " man").encode("utf-8"))


def main():
    ss = SpeechSynthesis()

    while True:
        ss.speak_random()
        time.sleep(5)

if __name__ == '__main__':
    main()
