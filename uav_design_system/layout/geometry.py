"""
file containing geometry
"""
from math import pi

class ThreeDimentional:
    pass

class Cuboid(ThreeDimentional):

    def __init__(self, x_size: float, y_size: float, z_size: float):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size

    @property
    def volume(self):
        return self.x_size * self.y_size * self.z_size

    @property
    def project_xy(self):
        pass

    @property
    def centroid(self):
        return Point(0.5*self.x_size, 0.5*self.y_size, 0.5*self.z_size)

    def _calc_interia(self, length, width):
        return ((length * length) + (width * width))/12

    @property
    def inertia_xx(self):
        """
        calculate the interial moment per unit mass about the objects centroid
        """
        return self._calc_interia(self.y_size, self.z_size)

    @property
    def inertia_yy(self):
        """
        calculate the interial moment per unit mass about the objects centroid
        """
        return self._calc_interia(self.x_size, self.z_size)

    @property
    def inertia_zz(self):
        """
        calculate the interial moment per unit mass about the objects centroid
        """
        return self._calc_interia(self.y_size, self.x_size)

    def reflect_y(self):
        """
        create a new object of this class but reflected in the y axis
        """
        return Cuboid(self.x_size, -1 * self.y_size, self.z_size)

class Cylinder(ThreeDimentional):

    def __init__(self, radius: float, y_size: float):
        self.radius = radius
        self.y_size = y_size

    @property
    def volume(self):
        return pi * self.radius * self.radius * self.y_size

    @property
    def centroid(self):
        return Point(0, 0.5 * self.y_size, 0)

    def calc_x_y_interias(self, radius, length):
        return (1/12)*(3*r*r + h*h)

    @property
    def inertia_xx(self):
        return (1/12)*(3*self.radius*self.radius + self.y_size*self.y_size)

    @property
    def inertia_zz(self):
        return self.inertia_xx

    @property
    def inertia_yy(self):
        return 0.5*self.radius*self.radius

    def reflect_y(self):
        """
        create a new object of this class but reflected in the y axis
        """
        return Cylinder(self.radius, -1 * self.y_size)


class TrapeziumPlate(ThreeDimentional):

    def __init__(self, x1_size, x2_size, x_shift, y_size, z_size):
        """
        trapezium with base x1, length y, thickness z and other base length x2
        """
        self.x1_size = x1_size
        self.x2_size = x2_size
        self.x_shift = x_shift
        self.y_size = y_size
        self.z_size = z_size #thickness size

    @property
    def volume(self):
        return 0.5*(self.x1_size + self.x2_size)*self.y_size*self.z_size

    @property
    def centroid(self):
        """
        """
        # get the difference between the two x lengths
        # calculation assuming a is the smallest length
        c = self.x_shift
        a = self.x2_size
        b = self.x1_size
        h = self.y_size

        x = (2 * a * c+ a * a + c * b + a * b + b * b)/(3 * (a + b))
        y = (h * ((2 * a) + b))/(3 * (a + b))
        z = 0.5 * self.z_size

        return Point(x, y, z)

    def _calc_interia(self, length, width):
        return ((length * length) + (width * width))/12

    @property
    def inertia_xx(self):
        """
        calculate the interial moment per unit mass about the objects centroid
        """
        return self._calc_interia(self.y_size, self.z_size)

    @property
    def inertia_yy(self):
        """
        calculate the interial moment per unit mass about the objects centroid
        """
        x_approx = 0.5 * (self.x1_size + self.x2_size)
        return self._calc_interia(x_approx, self.z_size)

    @property
    def inertia_zz(self):
        """
        calculate the interial moment per unit mass about the objects centroid
        """
        x_approx = 0.5 * (self.x1_size + self.x2_size)
        return self._calc_interia(self.y_size, x_approx)

    def reflect_y(self):
        return TrapeziumPlate(self.x1_size,
                              self.x2_size,
                              self.x_shift,
                              -1 * self.y_size,
                              self.z_size,)


class Point():

    def __init__(self, x: float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def as_tuple(self):
        return self.x, self.y, self.z

    def __eq__(self, value: 'Point'):
        """
        checks if two points are located at the same place
        """
        if self.x == value.x and self.y == value.y and self.z == value.z:
            is_equal = True
        else:
            is_equal = False

        return is_equal

    def __add__(self, value: 'Point'):

        x = self.x + value.x
        y = self.y + value.y
        z = self.z + value.z

        return Point(x, y, z)

    def reflect_y(self):
        return Point(self.x, -1 * self.y, self.z)
