from memes.ax12 import Ax12
from pyax12.connection import Connection

pyax12_connection = None
memes_connection = None

def init(port='/dev/serial0', baudrate=1000000, timeout=0.1,
                 waiting_time=0.02, rpi_gpio=True):
    pyax12_connection = Connection(port, baudrate, timeout, waiting_time, rpi_gpio)
    Ax12.port = pyax12_connection.serial_connection
    memes_connection = Ax12()

def read_temperature(id):
    memes_connection.readTemperature(id)