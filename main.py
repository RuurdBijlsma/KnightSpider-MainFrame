import threading
import ax12_serial
import time

import utils
from leg import Leg
from movement.sequences import sequences
from readings_worker import ReadingsWorker
from servo import Servo
from point import Point3D
from spider import Spider

Spider().start()
