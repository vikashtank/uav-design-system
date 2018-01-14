from os.path import dirname, abspath
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory)# so uggo thanks to atom runner
from .geometry import Point
import copy
from matplotlib import pyplot as plt

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


        self._location = Point(0, 0, 0)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: "Point"):
        self._location = value

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

    def flatten(self, name: str = ""):
        """
        converts an arrangement of nested arrangements and masses into an
        arrangement that only contains mass objects, where each mass object has
        had the location of its parent arrangements added to it.

        returns an arrangement with masses with global locations
        """
        def _all_mass_objects_global(arrangement):

            mass_list = []
            for object in arrangement:

                if isinstance(object, Arrangement):
                    new_mass_list = _all_mass_objects_global(object)
                    mass_list += new_mass_list
                else:
                    mass_list.append(object)

            # create copies so original instances are not editted
            cloned_list = [mass.clone() for mass in mass_list]
            # correct locations to add the arrangements
            for ob in cloned_list:
                ob.location += arrangement.location
            return cloned_list

        return Arrangement(name, *_all_mass_objects_global(self))

    @property
    def avl_mass_list(self):
        string_list = []
        for mass_object in self.all_mass_objects:
            string_list.append(mass_object.avl_mass_string)
        return string_list

    @property
    def total_mass(self):
        return sum(mass.mass for mass in self.all_mass_objects)


    @property
    def center_of_gravity(self):

        mom_x = sum(mass.mass * mass.center_of_gravity_global.x for mass in self.all_mass_objects)
        mom_y = sum(mass.mass * mass.center_of_gravity_global.y for mass in self.all_mass_objects)
        mom_z = sum(mass.mass * mass.center_of_gravity_global.z for mass in self.all_mass_objects)

        return Point(mom_x/self.total_mass,
                     mom_y/self.total_mass,
                     mom_z/self.total_mass)

    @property
    def center_of_gravity_global(self):
        return self.center_of_gravity + self.location

    def clone(self, reflect_y = False):
        """
        clone and return this object
        """
        clone = copy.deepcopy(self)
        if reflect_y:
            # change the locations of all points in the test_clone
            for mass in clone.all_mass_objects:
                mass.geometry = mass.geometry.reflect_y()
        return clone

    def __getitem__(self, value):

        val = [ob for ob in self.objects if ob.name == value]

        if not val:
            raise KeyError(f"no object in arrangement with name {value}")

        return val

    def __iter__(self):
        for ob in self.objects:
            yield ob

    def __len__(self):
        return len(self.objects)

    def plot_xy(self, subplot = None, center_of_gravity = False, marker = "b-"):
        """
        plots arrangement, optional centers of gravities of masses, key word
        arguments for matplotlib plot options
        """
        if subplot is None:
            plot = plt.subplot(111)

        for mass in self.all_mass_objects:
            x,y  = mass.geometry.project_xy.plot_coordinates
            subplot.plot(x, y, marker)

            if center_of_gravity:
                x, y, _ = mass.center_of_gravity_global.as_tuple()
                subplot.plot(x, y,"*")

        x, y, _ = self.center_of_gravity_global.as_tuple()
        subplot.plot(x, y, "o")

        return subplot



class MassObject(IsArrangeable):
    """
    represents a component
    """

    def __init__(self, geometry: 'ThreeDimentional', density: float, name = ""):
        self.name = name
        self.geometry = copy.deepcopy(geometry)
        self.density = density

    @property
    def mass(self):
        return self.geometry.volume * self.density

    def calc_weight(self, gravity):
        return self.mass * gravity

    @property
    def center_of_gravity(self):
        return self.geometry.centroid

    @property
    def center_of_gravity_global(self):
        return self.geometry.centroid + self.location

    @property
    def location(self):
        """
        get the global position of the origin of this object
        """
        return self.geometry.location

    @location.setter
    def location(self, value: 'Point'):
        """
        set the global position of the origin of this object
        """
        self.geometry.location = value

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

    def clone(self):
        return copy.deepcopy(self)

    def __eq__(self, value):

        return self.name == value.name and \
               self.location == value.location and \
               self.density == value.density and \
               self.center_of_gravity == value.center_of_gravity and \
               type(self.geometry) == type(value.geometry)




if __name__  == "__main__":
    pass
