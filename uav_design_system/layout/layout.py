from os.path import dirname, abspath
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory)# so uggo thanks to atom runner
from geometry import Point

class IsArrangeable:
    pass

class Arrangement(IsArrangeable):
    """
    class made of a number of arrangements and Components
    """
    def __init__(self, name: str = "", *objects: IsArrangeable):
        self.name = name

        # if no objects are provided create an empty list
        if objects:
            self.objects = objects
        else:
            self.objects = []


        self.location = Point(0, 0, 0)

    def append(self, value: IsArrangeable):
        self.objects.append(value)

    @property
    def all_mass_objects(self):

        def _all_mass_objects(objects):
            """
            generator of all mass objects contained within objects and all masses
            within objects
            """
            mass_list = []
            for object in objects:
                if isinstance(object, Arrangement):
                    mass_list += _all_mass_objects(object.objects)
                else:
                    mass_list.append(object)
            return mass_list

        return _all_mass_objects(self.objects)

    @property
    def avl_mass_list(self):
        string_list = []
        for mass_object in self.all_mass_objects:
            string_list.append(mass_object.avl_mass_string)
        return string_list

    @property
    def total_mass(self):
        total_mass = 0
        for mass in self.all_mass_objects:
            total_mass += mass.mass

        return total_mass

    @property
    def center_of_gravity(self):
        total_moment = 0
        for mass in self.all_mass_objects:
            total_moment += mass.mass * mass.center_of_gravity_global.x

        return total_moment/self.total_mass


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

    @property
    def center_of_gravity_global(self):
        return self._center_of_gravity + self._location

    @center_of_gravity.setter
    def center_of_gravity(self, value: 'Point'):
        self._center_of_gravity = value

    @property
    def location(self):
        """
        get the global position of the origin of this object
        """
        return self._location

    @location.setter
    def location(self, value: 'Point'):
        """
        set the global position of the origin of this object
        """
        self._location = value

    @property
    def inertia_xx(self):
        return self.geometry.inertia_xx * self.mass

    @property
    def inertia_yy(self):
        return self.geometry.inertia_yy * self.mass

    @property
    def inertia_zz(self):
        return self.geometry.inertia_zz * self.mass

    @property
    def avl_mass_string(self):
        """
        creates athena vortex lattice mass data string for .mass file
        """
        x,y,z = self.center_of_gravity_global.as_tuple()
        ixx, iyy, izz = self.inertia_xx, self.inertia_yy, self.inertia_zz
        template = "{0}   {1}   {2}   {3}    {4}   {5}   {6}".format(self.mass,
                                                                     x,
                                                                     y,
                                                                     z,
                                                                     ixx,
                                                                     iyy,
                                                                     izz)
        return template




if __name__  == "__main__":
    pass
