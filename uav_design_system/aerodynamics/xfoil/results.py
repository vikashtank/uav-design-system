"""
results from xfoil post processor
"""


class XfoilResults():

    def __init__(self, xfoil_results_dict):
        self._results_dict = xfoil_results_dict

    @property
    def _results_list(self):
        return self._results_dict["xfoil"]["analysis"]["results"]

    def get_closest_value(self, parameter_name, value):
        return min(self._results_list, key = lambda x: abs(x[parameter_name] - value))

    def get_min(self, parameter_name):
        return min(self._results_list, key = lambda x: x[parameter_name])

    def get_max(self, parameter_name):
        return max(self._results_list, key = lambda x: x[parameter_name])

    def get_closest_alpha(self, alpha: float):
        return self.get_closest_value("alpha", alpha)

    def get_closest_cl(self, value: float):
        return self.get_closest_value("cl", value)

    @property
    def lift_slope(self):
        results_list =  sorted(self._results_list, key = lambda x:x["alpha"])

        d_cl = results_list[1]["cl"] -  results_list[0]["cl"]
        d_alpha = results_list[1]["alpha"] -  results_list[0]["alpha"]

        return d_cl/d_alpha

    @property
    def cd0(self):
        return self.get_closest_value("cl", 0)["cd"]
