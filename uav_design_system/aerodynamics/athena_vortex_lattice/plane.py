import sys
import os
sys.path.append(os.path.dirname(__file__) + "/../../common")
from .surface import Surface, NoAerofoilError
from typing import List

class MainWingError(AttributeError):
    pass

class Plane():

    def __init__(self, name: str, *surfaces: List[Surface]):
        self.name = name
        self.surfaces = list(surfaces)
        self.x_ref = 0
        self.y_ref = 0
        self.z_ref = 0

    def __iter__(self):
        for i in self.surfaces:
            yield i

    def append(self, value: Surface):
        self.surfaces.append(value)

    @property
    def _ref_string(self):
        """
        string at the top of the avl input file with reference values
        """
        list = [f"{self.name}",
                "0.0                      Mach",
                "0     0     0.0          iYsym  iZsym  Zsym",
                f"{self.reference_area} {self.reference_cord}  {self.reference_span}          "
                "Sref   Cref   Bref   reference area, chord, span",
                f"{self.x_ref} {self.y_ref}   {self.z_ref}"
                "          Xref   Yref   Zref   moment reference location (arb.)",
                "0.020                    CDoref",
                "#"
                ]
        return "\n".join(list)

    @property
    def _to_avl_string(self):
        plane_string_list = [self._ref_string]
        for index, surface in enumerate(self):
            plane_string_list.append("#" + "=" * 62)
            surface_string = surface._to_avl_string(f"surf{index}_")
            plane_string_list.append(surface_string)
        return "\n".join(plane_string_list)

    def dump_avl_files(self, directory):
        # write .avl file
        avl_file = os.path.join(directory, f"{self.name}.avl")
        with open(avl_file, "w") as open_file:
            open_file.write(self._to_avl_string)

        aerofoil_files = self._write_aerofoil_files(directory)
        return avl_file, aerofoil_files

    def _write_aerofoil_files(self, directory):
        files = []
        for j, surface in enumerate(self):
            for i, section in enumerate(surface):
                try:
                    file_path = os.path.join(directory, f"surf{j}_sec{i}_af.txt")
                    files.append(self._write_aerofoil_file(file_path, section.aerofoil))
                except NoAerofoilError:
                    continue
        return files

    def _write_aerofoil_file(self, file_path, aerofoil):
        with open(file_path, "w") as open_file:
            aerofoil.write(open_file)
        return file_path

    @property
    def main_surface(self):
        return self.surfaces[0]

    @property
    def reference_area(self):
        return self.main_surface.area

    @property
    def reference_cord(self):
        return self.main_surface.cord

    @property
    def reference_span(self):
        return self.main_surface.span