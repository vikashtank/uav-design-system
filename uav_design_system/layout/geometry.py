"""
file containing geometry
"""

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
