"""
API for reading in AVL results
"""
import re

class AVLResults():

    def __init__(self, results_dict):
        self._results_dict = results_dict

    @property
    def _total_forces(self):
        return self._results_dict["total_forces"]

    def _get_reg_expression(self, parameter_name):
        return rf"{parameter_name}\s*=\s*(\d*\.\d*)"

    def extract_field(self, parameter_name):
        reg_exp = self._get_reg_expression(parameter_name)
        match = re.search(reg_exp, self._total_forces)
        return float(match.group(1))

    @property
    def alpha(self):
        return self.extract_field("Alpha")

    @property
    def elevator_deflection(self):
        return self.extract_field("elevator")

    @property
    def cl(self):
        return self.extract_field("CLtot")

    @property
    def cd(self):
        return self.extract_field("CDind")

    @property
    def efficiency(self):
        return self.extract_field("e")

    @property
    def surface_area(self):
        return self.extract_field("Sref")

    @property
    def cord(self):
        return self.extract_field("Cref")

    @property
    def Span(self):
        return self.extract_field("Bref")

    @property
    def cord_distribution(self):
        pass
