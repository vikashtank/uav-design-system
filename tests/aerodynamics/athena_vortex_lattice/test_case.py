from os.path import join, exists, dirname, abspath
from os import makedirs, remove
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.aerodynamics.athena_vortex_lattice as avl


def get_resource_content(file_name):
    """
    function to retrieve data from files in the resource folder for these tests
    """
    resources_directory = join(this_directory, "resources", "case_resources")
    with open(join(resources_directory, file_name)) as open_file:
        return open_file.read()


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

        expected_string = get_resource_content("case_to_file.txt")

        with open(file_name) as open_file:
            actual_string = open_file.read()
        self.maxDiff = None

        self.assertEqual(expected_string.strip(), actual_string.strip())
        remove(file_name)




if __name__ == "__main__":
    unittest.main()
