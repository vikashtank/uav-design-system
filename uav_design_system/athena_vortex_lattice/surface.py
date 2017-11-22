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

    def append(self, value):
        self._sections.append(value)

    def define_mesh(self, number_cord: int = 20, number_span: int = 40,
                    cord_distribution: float = 1, span_distribution: float = 1):
        self.number_cord = number_cord
        self.number_span = number_span
        self.cord_distribution = cord_distribution
        self.span_distribution = span_distribution

    def define_translation_bias(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def add_section(self, section: 'Section'):
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
        self.aerofoil = aerofoil

    def _add_control_surface(self, control_surface: 'ControlSurface'):
        self.control_surface = control_surface

    def translation_bias(self):
        pass

    def __str__(self):
        pass



class ControlSurface():

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
