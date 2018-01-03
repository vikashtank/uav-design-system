"""
script for creating run case files
"""

class InvalidCaseParamError(Exception):
    pass


class TrimCase():


    CASEPARAMETERS = {
        "cl": 0,
        "alpha": 0,
        "beta": 0,
        "pb/2v": 0,
        "qc/2v": 0,
        "rb/2v": 0,
        "cdo": 0,
        "bank": 0,
        "elevation": 0,
        "heading": 0,
        "mach": 0,
        "velocity": 1,
        "density": 1.225,
        "gravity": 9.81,
        "turn_radius": 0,
        "load factor": 1,
        "x cg": 0,
        "y cg": 0,
        "z cg": 0,
        "mass": 0,
        "ixx": 0,
        "iyy": 0,
        "izz": 0,
        "ixy": 0,
        "iyz": 0,
        "izx": 0,
        "visc cl a": 0,
        "visc cl u": 0,
        "visc cm a": 0,
        "visc cm u": 0,
    }

    ALIASDICT = {
        "cl": "CL",
        "alpha": "alpha",
        "beta": "beta",
        "pb/2v": "pb/2V",
        "qc/2v": "qc/2V",
        "rb/2v": "rb/2V",
        "cdo": "CDo",
        "bank": "bank",
        "elevation": "elevation",
        "heading": "heading",
        "mach": "Mach",
        "velocity": "velocity",
        "density": "density",
        "gravity": "grav.acc.",
        "turn_radius": "turn_rad.",
        "load factor": "load_fac.",
        "x cg": "X_cg",
        "y cg": "Y_cg",
        "z cg": "Z_cg",
        "mass": "mass",
        "ixx": "Ixx",
        "iyy": "Iyy",
        "izz": "Izz",
        "ixy": "Ixy",
        "iyz": "Iyz",
        "izx": "Izx",
        "visc cl a": "visc CL_a",
        "visc cl u": "visc CL_u",
        "visc cm a": "visc CM_a",
        "visc cm u": "visc CM_u",
    }


    def __init__(self, ref_area, **kwargs):

        self._case_parameters = TrimCase.CASEPARAMETERS
        self._ref_area = ref_area

        for kwarg in kwargs:
            self[kwarg] = kwargs[kwarg]

    def set_trim_cl(self, velocity, density, mass, gravity, area):
        self._case_parameters["cl"] = mass*gravity/(0.5*density*velocity*velocity*area)

    def __len__(self):
        return len(self._case_parameters)

    def __getitem__(self, key):
        self._missing(key)
        return self._case_parameters[key]

    def __setitem__(self, key, value):

        self._missing(key)

        self._case_parameters[key] = value

        if key == "cl":
            raise InvalidCaseParamError("cl cannot be directly set")

        self.set_trim_cl(self["velocity"],
                         self["density"],
                         self["mass"],
                         self["gravity"],
                         self._ref_area)

    def _missing(self, key):

        if key not in self._case_parameters:
            raise InvalidCaseParamError("""{0} is not  a valid case parameter/
            please see TrimCase.CASEPARAMETERS for full list with default
            values""".format(key))


    def to_file(self, file_name):

        top_string = """---------------------------------------------
 Run case  1:  0 deg. bank

 alpha        ->  CL          =  {0}
 beta         ->  Cl roll mom =   0.00000
 pb/2V        ->  pb/2V       =   0.00000
 qc/2V        ->  qc/2V       =   0.00000
 rb/2V        ->  rb/2V       =   0.00000
 elevator     ->  Cm pitchmom =   0.00000

""".format(self["cl"])

        bottom_string = ""

        for key, value in self._case_parameters.items():
            line = "{0} = {1}".format(TrimCase.ALIASDICT[key], value)
            bottom_string += (line + "\n")

        with open(file_name, "w") as open_file:
            open_file.write(top_string + bottom_string)







if __name__ == "__main__":
    pass
