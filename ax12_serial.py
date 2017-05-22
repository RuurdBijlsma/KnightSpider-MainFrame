from pyax12.connection import Connection

def init(self, port='/dev/serial0', baudrate=1000000, timeout=0.1,
                 waiting_time=0.02, rpi_gpio=True):
    pyax12_connection = Connection(port, baudrate, timeout, waiting_time, rpi_gpio)

