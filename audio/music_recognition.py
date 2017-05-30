#!/usr/bin/env python
# Written by Yu-Jie Lin
# Public Domain
#
# Deps: PyAudio, NumPy, and Matplotlib
# Blog: http://blog.yjl.im/2012/11/frequency-spectrum-of-sound-using.html

import struct
import sys
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

HEIGHT_MULTIPLIER = 10

ANIMATE = False
TITLE = ''
WIDTH = 1280
HEIGHT = 720
FPS = 60.0

nFFT = 512
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


def init_animation(line):
    # This data is a clear frame for animation
    line.set_ydata(np.zeros(nFFT - 1))
    return line,


def animate(i, line, stream, wf, MAX_y):
    # Read n*nFFT frames from stream, n > 0
    N = max(stream.get_read_available() / nFFT, 1) * nFFT
    data = stream.read(int(N))

    # Unpack data, LRLRLR...
    y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
    y_L = y[::2]
    y_R = y[1::2]

    Y_L = np.fft.fft(y_L, nFFT)
    Y_R = np.fft.fft(y_R, nFFT)

    # Sewing FFT of two channels together, DC part uses right channel's
    indexL = int(-nFFT / 2)
    indexR = int(nFFT / 2)
    temp1 = (Y_L[indexL:-1], Y_R[:indexR])
    temp2 = np.hstack(temp1)
    Y = abs(temp2)

    line.set_ydata(Y)
    return line,


def print_star(n, symbol="="):
    if (n > 0):
        sys.stdout.write(symbol)
        print_star(n - 1)
    else:
        sys.stdout.write("\n")


def average(list):
    return sum(list) / len(list)


def tick(stream, MAX_y):
    # Read n*nFFT frames from stream, n > 0
    N = max(stream.get_read_available() / nFFT, 1) * nFFT
    data = stream.read(int(N))

    # Unpack data, LRLRLR...
    y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
    values = np.fft.fft(y, nFFT)

    range_start = 0
    multiplier = 30
    range_end = 0.1

    end_index = int(range_end * len(values))
    print_star(int(average(values[range_start:end_index]) * multiplier))
    # threading.Timer(1 / FPS, lambda: tick(stream, MAX_y)).start()


def main():
    dpi = plt.rcParams['figure.dpi']
    plt.rcParams['savefig.dpi'] = dpi
    plt.rcParams["figure.figsize"] = (1.0 * WIDTH / dpi, 1.0 * HEIGHT / dpi)

    fig = plt.figure()

    # Frequency range
    x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE
    ax = fig.add_subplot(111, title=TITLE, xlim=(x_f[0], x_f[-1]),
                         ylim=(0, 2 * np.pi * nFFT ** 2 / RATE))
    ax.set_yscale('symlog', linthreshy=nFFT ** 0.5)

    line, = ax.plot(x_f, np.zeros(nFFT - 1))

    py_audio = pyaudio.PyAudio()
    # Used for normalizing signal. If use paFloat32, then it's already -1..1.
    # Because of saving wave, paInt16 will be easier.
    MAX_y = 2.0 ** (py_audio.get_sample_size(FORMAT) * 8 - 1)
    MAX_y /= HEIGHT_MULTIPLIER

    stream = py_audio.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=BUF_SIZE)

    if (ANIMATE):
        frames = None
        wf = None

        ani = animation.FuncAnimation(
            fig, animate, frames,
            init_func=lambda: init_animation(line), fargs=(line, stream, wf, MAX_y),
            interval=1000.0 / FPS, blit=True
        )
        plt.show()
    else:
        while (True):
            tick(stream, MAX_y)
            time.sleep(1 / FPS)

    stream.stop_stream()
    stream.close()
    py_audio.terminate()


if __name__ == '__main__':
    main()
