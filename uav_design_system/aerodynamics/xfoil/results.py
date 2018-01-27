"""
results from xfoil post processor
"""



class AerofoilResults():

    def __init__(self, xfoil_results_dict):
        self._results_dict = xfoil_results_dict

    @property
    def _results_list(self):
        return self._results_dict["xfoil"]["analysis"]["results"]

    def _get_value(self, parameter_name, value):
        return min(self._results_list, key = lambda x: abs(x[parameter_name] - value))

    def _get_min(self, parameter_name):
        return min(self._results_list, key = lambda x: x[parameter_name])

    def _get_max(self, parameter_name):
        return max(self._results_list, key = lambda x: x[parameter_name])

    def get_alpha(self, alpha: float):
        return self._get_value("alpha", alpha)

    def get_cl(self, value: float):
        return self._get_value("cl", value)

    @property
    def lift_slope(self):
        results_list =  sorted(self._results_list, key = lambda x:x["alpha"])

        d_cl = results_list[1]["cl"] -  results_list[0]["cl"]
        d_alpha = results_list[1]["alpha"] -  results_list[0]["alpha"]

        return d_cl/d_alpha

    @property
    def cd0(self):
        return self._get_value("cl", 0)["cd"]
