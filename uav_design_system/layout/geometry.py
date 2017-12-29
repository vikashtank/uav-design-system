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

class Cylinder(ThreeDimentional):

    def __init__(self, radius: float, z_size: float):
        self.radius = radius
        self.z_size = z_size

    @property
    def volume(self):
        return pi * self.radius * self.radius * self.z_size

    @property
    def centroid(self):
        return Point(0, 0, 0.5 * self.z_size)

    def calc_x_y_interias(self, radius, length):
        return (1/12)*(3*r*r + h*h)

    @property
    def inertia_xx(self):
        return (1/12)*(3*self.radius*self.radius + self.z_size*self.z_size)

    @property
    def inertia_yy(self):
        return self.inertia_xx

    @property
    def inertia_zz(self):
        return 0.5*self.radius*self.radius

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
