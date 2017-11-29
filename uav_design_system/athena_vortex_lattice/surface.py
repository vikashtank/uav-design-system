import collections
from enum import Enum
from typing import List


class Surface():
    """
    Class responsible for all aerodynamic surfaces, such as wings or rudders
    """

    name: str
    reflect_surface: bool
    bias_angle: float

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.reflect_surface = False
        self.angle_bias = 0
        self.sections = []

        #default all values
        self.define_mesh()
        self.define_translation_bias()


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

        return total_area

    @property
    def cord(self):
        """
        returns the maximum cord of the sections in this surface
        """
        cord = 0
        for section in self.sections:
            if section.cord > cord:
                cord = section.cord

        return cord

    @property
    def span(self):
        """
        returns the maximum y distance from wing center of the sections in this surface
        """
        span = 0

        for section in self:
            if section.y > span:
                span = section.y

        return span



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
        origin. defaulted to the global origin

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
        for index, section in enumerate(self.sections):
            if start_section <= index <= end_section:
                section._add_control_surface(control_surface)

    def __getitem__(self, key):
        return self.sections[key]


    @property
    def _ref_string(self):
        string = """
all
0.0                      Mach
0     0     0.0          iYsym  iZsym  Zsym
0.68 6.6  78.6          Sref   Cref   Bref   reference area, chord, span
3.250 0.0   0.5          Xref   Yref   Zref   moment reference location (arb.)
0.020                    CDoref
#
#==============================================================
"""

        return string


    @property
    def _top_string(self):
        string  = """
#
SURFACE
WINGly
20  1.0  30  1.0  !  Nchord   Cspace   Nspan  Sspace
#
# reflect image wing about y=0 plane
YDUPLICATE
     0.00000
#
# twist angle bias for whole surface
ANGLE
     0.00000
#
# x,y,z bias for whole surface
TRANSLATE
    0.00000     0.00000     0.00000
"""

    def __str__(self):
        pass


class Section():


    def __init__(self, aerofoil_file_path: str, cord: float):
        self.add_aerofoil(aerofoil_file_path)
        self.cord = cord
        self.x = 0
        self.y = 0
        self.z = 0
        self.twist_angle = 0

    def add_aerofoil(self, aerofoil_file_path: str):
        self.aerofoil = aerofoil_file_path

    def _add_control_surface(self, control_surface: 'ControlSurface'):
        self.control_surface = control_surface

    def translation_bias(self, x, y, z):
        """
        The location of the top of the cord of this section
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):

        try:
            control_surface = "CONTROL\n" + str(self.control_surface)
        except AttributeError:
            control_surface = ""

        try:
            aerofoil = self.aerofoil
        except AttributeError:
            aerofoil = ""


        string = """#    Xle         Yle         Zle         chord       angle   Nspan  Sspace
SECTION
     {0}     {1}     {2}     {3}         {4}
{5}
AFIL
{6}
""".format(self.x,
           self.y,
           self.z,
           self.cord,
           self.twist_angle,
           str(control_surface),
           aerofoil)

        return string



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

    def __str__(self):
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
