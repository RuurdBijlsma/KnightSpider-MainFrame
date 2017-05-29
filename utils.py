import math
import subprocess
from subprocess import check_output


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
    ps = subprocess.Popen(('ps', '-A'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', 'process_name'), stdin=ps.stdout)
    ps.wait()


def get_cpu_temp():
    return round(
        int(check_output([
            "cat",
            "/sys/class/thermal/thermal_zone0/temp"
        ])) / 1000,
        2
    )
