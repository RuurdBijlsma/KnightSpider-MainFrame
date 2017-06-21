import json


class ServoReadings(object):
    LOAD_MASK = 0b1000000000

    def __init__(self, id, position=-1, load=-1, voltage=-1, temperature=-1):
        self.id = id
        self.temperature = temperature
        self.voltage = voltage

        load_direction = load & self.LOAD_MASK
        load_value = load & ~self.LOAD_MASK

        self.load_direction = load_direction
        self.load = load_value
        self.position = position

        # if voltage < 7.5:
        #     print("voltage low: {} at id {}".format(self.voltage, self.id))
        # elif voltage > 11:
        #     print("voltage high: {} at id {}".format(self.voltage, self.id))

    def __str__(self):
        return "Readings for {4}:\nTemperature = {0}\nVoltage = {1}\nLoad = {2}\nPosition = {3}\n".format(
            self.temperature,
            self.voltage,
            self.load,
            self.position,
            self.id
        )

    def to_json(self):
        return json.dumps(
            {
                "id": self.id,
                "temperature": self.temperature,
                "voltage": self.voltage,
                "load": self.load,
                "position": self.position
            },
            separators=(",", ":")
        )

    @staticmethod
    def empty():
        return ServoReadings(
            position=-500,
            voltage=-500,
            temperature=-500,
            load=-500,
            id=-1,
        )


class SpiderInfo(object):
    def __init__(self, battery_level=-1, slope=-1, cpu_usage=-1, cpu_temperature=1):
        self.cpu_temperature = cpu_temperature
        self.cpu_usage = cpu_usage
        self.slope = slope
        self.battery_level = battery_level

    def to_json(self):
        return json.dumps({
            "battery": self.battery_level,
            "slope": self.slope,
            "cpuUsage": self.cpu_usage,
            "cpuTemperature": self.cpu_temperature
        })
