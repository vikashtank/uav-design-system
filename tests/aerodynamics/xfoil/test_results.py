from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system.aerodynamics.xfoil import XfoilResults
import json

class TestCase(unittest.TestCase):

    def setUp(self):
        comparison_json = join(this_directory, "resources", "test_results.json")
        with open(comparison_json) as open_file:
            self.expected_json = json.load(open_file)

        self.aerofoil_results = XfoilResults(self.expected_json)

    def test_get_value_exact(self):
        expected = {"alpha": 0.0, "cl": 0.0, "cd": 0.00581, "cm": 0.0}
        self.assertEqual(self.aerofoil_results.get_closest_value("alpha", 0), expected)

        expected = {"alpha": 2.5, "cl": 0.2108, "cd": 0.0065, "cm": 0.0165}
        self.assertEqual(self.aerofoil_results.get_closest_value("cl", 0.2108), expected)

    def test_get_value_almost_exact(self):
        expected = {"alpha": 0.0, "cl": 0.0, "cd": 0.00581, "cm": 0.0}
        self.assertEqual(self.aerofoil_results.get_closest_value("alpha", 0.2), expected)

        expected = {"alpha": 2.5, "cl": 0.2108, "cd": 0.0065, "cm": 0.0165}
        self.assertEqual(self.aerofoil_results.get_closest_value("cl", 0.22), expected)

    def test_max(self):
        expected = {"alpha": 5.0, "cl": 0.4525, "cd": 0.00848, "cm": 0.0253}
        self.assertEqual(self.aerofoil_results.get_max("alpha"), expected)

    def test_max(self):
        expected = {"alpha": 0.0, "cl": 0.0, "cd": 0.00581, "cm": 0.0}
        self.assertEqual(self.aerofoil_results.get_min("alpha"), expected)

    def test_cd0(self):
        self.assertEqual(self.aerofoil_results.cd0, 0.00581)

    def test_lift_slope(self):
        self.assertEqual(self.aerofoil_results.lift_slope, 0.0828)

    def test_get_value_list(self):
        actual_list = self.aerofoil_results.get_value_list('alpha')
        self.assertEqual(actual_list, [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

    def test_interpolation(self):
        interpolation = self.aerofoil_results.get_interpolation('alpha', 'cl', kind = 'cubic')
        self.assertEqual(interpolation(2.5), 0.2108)

    def test_lift_alpha_curve(self):
        interpolation = self.aerofoil_results.get_lift_alpha_curve( kind = 'cubic')
        self.assertEqual(interpolation(2.5), 0.2108)




if __name__ == "__main__":
    unittest.main()
