from os.path import join, exists, dirname, abspath
from os import makedirs, remove
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.athena_vortex_lattice as avl


class TestCase(unittest.TestCase):


    def setUp(self):
        pass

    def test_kwargs(self):
        """
        tests that key word arguments update the case parameter dictionary
        """
        trim_case = avl.TrimCase(1, velocity = 5)
        self.assertEqual(trim_case._case_parameters["velocity"], 5)

    def test_missing_kwarg_instance(self):
        """
        test that an invalid kwarg raises an error when instancing
        """
        try:
            trim_case = avl.TrimCase(1, hey = 5)
        except avl.InvalidCaseParamError:
            pass

    def test_missing_kwarg(self):
        """
        test that an invalid kwarg raises an error
        """
        trim_case = avl.TrimCase(1, velocity = 5)

        try:
            trim_case["hey"] = 5
        except avl.InvalidCaseParamError:
            pass

    def test_error_setting_cl(self):
        """
        test that an invalid kwarg raises an error
        """
        trim_case = avl.TrimCase(1, velocity = 5)

        try:
            trim_case["cl"] = 5
        except avl.InvalidCaseParamError:
            pass

    def test_error_getting_missing_param(self):
        """
        test that an invalid kwarg raises an error
        """
        trim_case = avl.TrimCase(1, velocity = 5)

        try:
            trim_case["hey"]
        except avl.InvalidCaseParamError:
            pass


    def test_cl_update(self):
        """
        test that the coefficient of lift updates when kwargs update
        """
        trim_case = avl.TrimCase(1, velocity = 1, mass = 1, gravity = 1, density = 1)
        self.assertEqual(trim_case["cl"], 2)


    def test_to_file_exists(self):

        file_name = join(this_directory, "test_file.txt")
        trim_case = avl.TrimCase(1)
        trim_case.to_file(file_name)
        self.assertTrue(exists(file_name))

        remove(file_name)

    def test_to_file_content(self):

        file_name = join(this_directory, "test_file.txt")
        trim_case = avl.TrimCase(1)
        trim_case.to_file(file_name)

        expected_string = """---------------------------------------------
 Run case  1:  0 deg. bank

 alpha        ->  CL          =  0.08
 beta         ->  Cl roll mom =   0.00000
 pb/2V        ->  pb/2V       =   0.00000
 qc/2V        ->  qc/2V       =   0.00000  s
 rb/2V        ->  rb/2V       =   0.00000
 elevator     ->  Cm pitchmom =   0.00000

CL = 0.08
alpha = 0
beta = 0
pb/2V = 0
qc/2V = 0
rb/2V = 0
CDo = 0
bank = 0
elevation = 0
heading = 0
Mach = 0
velocity = 5
density = 1
grav.acc. = 1
turn_rad. = 0
load_fac. = 1
X_cg = 0
Y_cg = 0
Z_cg = 0
mass = 1
Ixx = 0
Iyy = 0
Izz = 0
Ixy = 0
Iyz = 0
Izx = 0
visc CL_a = 0
visc CL_u = 0
visc CM_a = 0
visc CM_u = 0
"""

        with open(file_name) as open_file:
            actual_string = open_file.read()

        self.assertEqual(expected_string.strip(), actual_string.strip())
        remove(file_name)


if __name__ == "__main__":
    unittest.main()
