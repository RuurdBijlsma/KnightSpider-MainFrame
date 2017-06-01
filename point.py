class Point3D(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def negate_x(self):
        return Point3D(
            -self.x,
            self.y,
            self.z
        )

    def negate_y(self):
        return Point3D(
            self.x,
            -self.y,
            self.z
        )

    def negate_z(self):
        return Point3D(
            self.x,
            self.y,
            -self.z
        )

    def negate(self):
        return Point3D(
            -self.x,
            -self.y,
            -self.z
        )

    @staticmethod
    def from_string(str):
        arr = str.split(',')
        return Point3D(arr[0], arr[1], arr[2])

    def __str__(self):
        return "{0},{1},{2}".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(str(self))
