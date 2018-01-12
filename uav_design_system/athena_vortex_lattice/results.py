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
    def _hinge_forces(self):
        return self._results_dict["hinge_moments"]

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

    def _get_strip_re_exp(self, column_number):
        return "^\s*\d*" + f"\s*{self._number_exp}" * column_number + f"\s*({self._number_exp})"

    def _get_distribution(self, column_number):
        lines = self._strip_forces.split("\n")
        return_list = []
        for line in lines:
            match = re.match(self._get_strip_re_exp(column_number), line)
            if match is not None:
                return_list.append(float(match.group(1)))
        return return_list

    @property
    def y_distribution(self):
        return self._get_distribution(0)

    @property
    def cord_distribution(self):
        return self._get_distribution(1)

    @property
    def area_distribution(self):
        return self._get_distribution(2)

    @property
    def cl_distribution(self):
        return self._get_distribution(6)

    @property
    def cd_distribution(self):
        return self._get_distribution(7)

    @property
    def cm_quarter_cord_distribution(self):
        return self._get_distribution(9)

    @property
    def elevator_hinge_coefficient(self):
        reg_ex = r"\s*elevator\s*(.*)"
        match = re.search(reg_ex, self._hinge_forces)
        return float(match.group(1))



if __name__ == "__main__":
    pass
