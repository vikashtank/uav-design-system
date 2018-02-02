import collections
from enum import Enum
from typing import List
from os.path import join
from matplotlib import pyplot as plt


class NoControlSurfaceError(Exception):
    pass

class NoSectionError(Exception):
    pass

class NoAerofoilError(Exception):
    pass


class Surface():
    """
    Class responsible for all aerodynamic surfaces, such as wings or rudders
    """

    name: str
    reflect_surface: bool
    bias_angle: float

    def __init__(self, name):
        self.name = name
        self.reflect_surface = False
        self.angle_bias = 0
        self.sections = []

        #default all values
        self.define_mesh()
        self.define_translation_bias()
        self.x_ref = 0
        self.y_ref = 0
        self.z_ref = 0

    @property
    def area(self):
        """
        gives the 2D plan view area of the wing
        """
        total_area = 0
        for i in range(len(self.sections) - 1):
            section = self.sections[i]
            next_section = self.sections[i + 1]

            height = 0.5*(section.cord + next_section.cord)
            length = next_section.y - section.y

            area = height * length
            total_area += area

        # if the wing is reflected take into account additional surface area
        reflection_factor = int(self.reflect_surface) + 1

        return total_area * reflection_factor

    @property
    def cord(self):
        """
        returns the maximum cord of the sections in this surface
        """
        return max(self.sections, key = lambda x:x.cord).cord

    @property
    def span(self):
        """
        returns the maximum y distance from wing center of the sections in this surface
        """
        # if the wing is reflected take into account additional span length
        reflection_factor = int(self.reflect_surface) + 1

        return max(self, key = lambda x:x.y).y * reflection_factor

    @property
    def x_reference_coordinate(self):
        """
        gets the location of the x reference coordinate from a percentage of the cord
        """
        return self.x_ref

    @x_reference_coordinate.setter
    def x_reference_coordinate(self, value):
        """
        input value as percentage of the cord
        """
        self.x_ref =  value*self.cord

    def define_mesh(self, number_cord: int = 20, number_span: int = 40,
                    cord_distribution: float = 1, span_distribution: float = 1):
        """
        define the number of grid lines and their distribution on the surface.

        inputs:
            number_cord: number of grid lines the cord is divided into
            number_span: number of grid lines the span is divided into
            cord_distribution: A number from 3 to -3, 3 being equal spacing
                                2 being sinusoidal spacing
                                1 being cosine spacing
                                Please see documentation for athena vortex lattice
                                for more information
            span_distribution: The same as cord distribution but along the span
        """
        self.number_cord = number_cord
        self.number_span = number_span
        self.cord_distribution = cord_distribution
        self.span_distribution = span_distribution

    def define_translation_bias(self, x: float = 0, y: float = 0, z: float = 0):
        """
        define the location of the origin of the wing compared to the global
        origin. defaulted to the global origin (0, 0, 0)

        inputs:
            x: location downstream, along velocity vector
            y: location along span.
            z: location upwards.
        """
        self.x = x
        self.y = y
        self.z = z

    def add_section(self, *sections: List['Section']):
        """
        add a section to the surface
        """
        for section in sections:
            self.sections.append(section)

    def __iter__(self):
        for i in self.sections:
            yield i

    def add_control_surface(self, control_surface: 'ControlSurface',
                            start_section: int, end_section: int):
        """
        add a control surface to this surface

        Inputs:
            control_surface: control surface instance
            start_section: the section the control surface starts at
            end_section: the section the control surface ends at

        Returns:
            None
        """
        try:
            for index in range(start_section, end_section + 1):
                    self.sections[index].control_surface = control_surface
        except IndexError:
            raise NoSectionError(f"invalid index range {start_section} "
                                 "to {end_section} : sections within "
                                 "range do not exist")

    def __getitem__(self, key):
        return self.sections[key]


    @property
    def _surface_string(self):
        """
        add surface information to the avl input string
        """
        if self.reflect_surface:
            y_duplicate_string = f"YDUPLICATE\n     0"
        else:
            y_duplicate_string = ""

        list  = ["#",
                 "SURFACE",
                 f"{self.name}",
                 f"{self.number_cord}  {self.cord_distribution}"
                 f"  {self.number_span}  {self.span_distribution}"
                 "  !  Nchord   Cspace   Nspan  Sspace",
                 "#",
                 "# reflect image wing about y=0 plane",
                 y_duplicate_string,
                 "#",
                 "# twist angle bias for whole surface",
                 "ANGLE",
                 f"     {self.angle_bias}",
                 "#",
                 "# x,y,z bias for whole surface",
                 "TRANSLATE",
                 f"    {self.x}     {self.y}     {self.z}",
                 "#" + "-" * 62,
                ]

        return "\n".join(list)


    def _to_avl_string(self, prefix = ""):
        surface_string = self._surface_string
        # add section strings
        for i, section in enumerate(self.sections):
            list = [section._to_avl_string(f"{prefix}sec{i}_af.txt"),
                    "#" + "-" * 23,
                    ]
            surface_string += ("\n" + "\n".join(list))

        return surface_string

    def __len__(self):
        return len(self.sections)

    def get_plot_coordinates(self):
        """
        gets x and y coordinate lists for plotting
        """

        le_x, le_y, le_z = [], [], []
        te_x, te_y, te_z = [], [], []

        for section in self:
            x, y, z = section.leading_edge_coordinates
            le_x.append(x)
            le_y.append(y)
            le_z.append(z)
            x, y, z = section.trailing_edge_coordinates
            te_x.append(x)
            te_y.append(y)
            te_z.append(z)

        x = le_x + te_x[::-1]
        y = le_y + te_y[::-1]
        z = le_z + te_z[::-1]

        if self.reflect_surface:
            x = x + x[::-1]
            y = y + [ -1 * i for i in y[::-1]]
            z = z + z[::-1]

        return x, y, z

    def plot_xy(self, subplot = None, marker = "g_"):

        if subplot is None:
            subplot = plt.subplot(111)
        x, y, _ = self.get_plot_coordinates()
        subplot.plot(x, y, marker)
        return subplot

    def _write_aerofoil_files(self, directory):
        files = []
        for i, section in enumerate(self):
            try:
                aerofoil_file = join(directory, f"section{i}_aerofoil.txt")
                with open(aerofoil_file, "w") as open_file:
                    section.aerofoil.write(open_file)
                files.append(aerofoil_file)
            except NoAerofoilError:
                continue
        return files


class Section():

    def __init__(self, cord: float):
        self.cord = cord
        self.x = 0
        self.y = 0
        self.z = 0
        self.twist_angle = 0
        self._control_surface = None
        self._aerofoil = None

    @property
    def aerofoil(self):
        if self._aerofoil:
            return self._aerofoil
        else:
            raise NoAerofoilError

    @aerofoil.setter
    def aerofoil(self, aerofoil: "Aerofoil"):
        self._aerofoil = aerofoil

    @property
    def control_surface(self):
        if self._control_surface:
            return self._control_surface
        else:
            raise NoControlSurfaceError

    @control_surface.setter
    def control_surface(self, control_surface: 'ControlSurface'):
        self._control_surface = control_surface

    def translation_bias(self, x, y, z):
        """
        The location of the top of the cord of this section
        """
        self.x = x
        self.y = y
        self.z = z

    @property
    def leading_edge_coordinates(self):
        return self.x, self.y, self.z

    @property
    def trailing_edge_coordinates(self):
        return self.x + self.cord, self.y, self.z

    def _to_avl_string(self, aerofoil_file_name):

        try:
            control_surface_string = self.control_surface.to_avl_string()
            control_surface = f"CONTROL\n{control_surface_string}"
        except NoControlSurfaceError:
            control_surface = ""

        lines = ["#    Xle         Yle         Zle         chord       angle   "
                 "Nspan  Sspace",
                 "SECTION",
                 f"     {self.x}     {self.y}     {self.z}     {self.cord}"
                 f"         {self.twist_angle}",
                 f"{control_surface}",
                 "AFIL",
                 f"{aerofoil_file_name}"]

        return "\n".join(lines)


class ControlSurface():
    """
    a control surface class

    inputs:
        name: give a name to the control surface for identification
        xhinge: the percentage of the cord this surface will take up
        deflection_type: the type of control surface: flaps or elevators
        gain: for the calculations of derivatives, this can be tuned to
              how much the surface moves in response to inputs
    """

    def __init__(self, name: str, xhinge: float,
                       rotation_axis: List[float],
                       deflection_type: 'ControlDeflectionType',
                       gain: float = 1):
        self.name = name
        self.xhinge = xhinge
        self.rotation_axis = rotation_axis
        self.deflection_type = deflection_type
        self.gain = gain

    def to_avl_string(self):
        """
        represents class as a string type for AVL use in .avl file
        """

        string = "{0}  {1}  {2}   {3} {4} {5}   {6}".format(
                                                    self.name,
                                                    self.gain,
                                                    self.xhinge,
                                                    self.rotation_axis[0],
                                                    self.rotation_axis[1],
                                                    self.rotation_axis[2],
                                                    self.deflection_type.value)

        return string

    def __str__(self):
        return self.to_avl_string()



class ControlDeflectionType(Enum):
    """
    Controls if a duplicated control surface (due to symmetry) deflects in
    the same direction or not:

    eg: aeilerons deflect in opposite directions so they are antisymetric, while
        elevators deflect in the same direction so they are symmetric
    """
    SYMMETRIC = 1
    ANTISYMETRIC = -1




if __name__ == "__main__":
    pass
