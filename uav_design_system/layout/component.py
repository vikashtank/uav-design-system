"""
takes geometry and mass objects and creates componentns such as beams and
structures
"""
from enum import Enum
from os.path import dirname, abspath
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory)# so uggo thanks to atom runner
from . import masses
from . import geometry


class StructuralModelType(Enum):
    """
    Used for selection of the structural model to be applied to wing
    """
    HOLLOWFOAM = 1

class StructuralModel(masses.Arrangement):

    def __init__(self, name = "", *objects):
        super().__init__(name, *objects)


class FoamSection(masses.MassObject):

    FOAMDENSITY = 5

    def __init__(self, x1: float, x2: float, x_shift: float, y: float,
                 thickness: float, name: str = ""):
        trapezium_plate = geometry.TrapeziumPlate(x1, x2, x_shift, y, thickness)
        super().__init__(trapezium_plate, FoamSection.FOAMDENSITY, name)


class StructureFactory():
    """
    builds wing structures from surface classes
    """

    def __init__(self, model: StructuralModel):
        self.model = model

    def __call__(self, surface: "Surface", *args, **kwargs):
        if self.model == StructuralModelType.HOLLOWFOAM:
            structure = self._create_foam_wing(surface, *args, **kwargs)

        return structure

    def _create_foam_wing(self, surface: "Surface", wall_thickness: float):
        """
        takes a surface class and applies a structure model, returning a wing
        structure class
        """

        foam_model = StructuralModel(surface.name)

        # loop through pairs of sections and create foam sections
        for index in range(len(surface) - 1):
            section1 = surface.sections[index]
            section2 = surface.sections[index + 1]

            name = "Section {0}".format(index)
            x1 = section1.cord
            x2 = section2.cord
            y = section2.y - section1.y
            x_shift = section1.x - section2.x
            thickness = wall_thickness * 2

            section = FoamSection(x1, x2, x_shift, y, thickness, name)
            section.location = geometry.Point(section1.x,
                                              section1.y,
                                              section1.z)

            foam_model.append(section)

        return foam_model


if __name__ == "__main__":
    pass
