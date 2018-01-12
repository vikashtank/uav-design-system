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

    @property
    def _strip_forces(self):
        return self._results_dict["strip_forces"]

    @property
    def _number_exp(self):
        return "-?\d*\.\d*"

    def _get_reg_expression(self, parameter_name):
        return f"{parameter_name}\s*=\s*({self._number_exp})"

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

    def _get_strip_re_exp(self):
        return "^\s*\d*" + f"\s*({self._number_exp})"


    @property
    def y_distribution(self):

        lines = self._strip_forces.split("\n")
        for line in lines:
            match = re.match(self._get_strip_re_exp(), line)
            if match is not None:
                yield float(match.group(1))







if __name__ == "__main__":
    pass
