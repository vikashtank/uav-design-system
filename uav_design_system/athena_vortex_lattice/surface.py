import collections
from enum import Enum
from typing import List


class Surface(collections.UserList):
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

    def add_section(self, section: 'Section'):
        """
        add a section to the surface
        """
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

    def __str__(self):
        pass

class Section():

    def __init__(self):
        pass

    def add_aerofoil(self, aerofoil_file_path: str):
        self.aerofoil = aerofoil_file_path

    def _add_control_surface(self, control_surface: 'ControlSurface'):
        self.control_surface = control_surface

    def translation_bias(self):
        pass

    def __str__(self):
        pass



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
        pass


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
