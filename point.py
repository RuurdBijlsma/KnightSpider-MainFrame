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

    def __str__(self):
        return "x:{0}, y:{1}, z:{2}".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(str(self))
