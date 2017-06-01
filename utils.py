import math
from subprocess import check_output

import psutil


# from point import Point3D


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def get_cpu_usage():
    return psutil.cpu_percent()


def get_cpu_temp():
    return round(
        int(check_output([
            "cat",
            "/sys/class/thermal/thermal_zone0/temp"
        ])) / 1000,
        2
    )
