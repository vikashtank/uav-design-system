

class IsArrangeable:
    pass


class Arrangement(IsArrangeable):
    """
    class made of a number of arrangements and Components
    """
    def __init__(self, name: str = "", *objects: IsArrangeable):
        self.name = name
        self.objects = objects

class MassObject(IsArrangeable):
    """
    represents a component
    """

    def __init__(self, geometry: 'ThreeDimentional', density: float, name = ""):
        self.name = name
        self.geometry = geometry
        self.density = density
        self._center_of_gravity = self.geometry.centroid
        self._location = Point(0, 0, 0)

    @property
    def mass(self):
        return self.geometry.volume * self.density

    def calc_weight(self, gravity):
        return self.mass * gravity

    @property
    def center_of_gravity(self):
        return self._center_of_gravity

    @center_of_gravity.setter
    def center_of_gravity(self, value: 'Point'):
        self._center_of_gravity = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: 'Point'):
        self._location = value





if __name__  == "__main__":
    pass
