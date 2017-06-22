import threading


class DanceMover(object):
    def __init__(self, spider, dance_sequence):
        self.spider = spider
        self.dance_sequence = dance_sequence
        self.index = 0
        self.cancel = False
        self.is_playing = False

    def execute(self):
        self.is_playing = True

        if self.index > len(self.dance_sequence) - 1:
            print("finished dance")
            self.cancel = True

        if self.cancel:
            self.index = 0
            self.cancel = False
            return

        stance, time, servo_speed = self.dance_sequence[self.index]
        self.index += 1

        self.spider.speed = servo_speed
        self.spider.leg_mover.set_stance(stance, enable_ground_clearance=False)

        threading.Timer(time, self.execute).start()

    def cancel(self):
        self.cancel = True