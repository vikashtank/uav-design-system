import os
this_directory = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")
import unittest
from uav_design_system.xfoil import XfoilRunner
import shutil
import json


class Test(unittest.TestCase):


    def setUp(self):
        self.results_dir = os.path.join(this_directory, "results_dir")
        try:
            shutil.rmtree(self.results_dir)
        except FileNotFoundError:
            pass

        # read the results file that is expected to be produced
        comparison_file = os.path.join(this_directory, "resources", "aerofoil_results.txt")
        comparison_json = os.path.join(this_directory, "resources", "expected_results.json")
        self.aerofoil_file = os.path.join(this_directory, "resources", "test_aerofoil.txt")

        with open(comparison_file) as open_file:
            self.expected_content = open_file.read()

        with open(comparison_json) as open_file:
            self.expected_json = json.load(open_file)

    def tearDown(self):
        shutil.rmtree(self.results_dir)

    def test_run_success(self):

        file_path = "/Applications/Xfoil.app/Contents/Resources/xfoil"

        os.makedirs(self.results_dir)

        xfoil_runner = XfoilRunner(file_path)
        xfoil_runner.setup_analysis(self.aerofoil_file, 1e6)
        results = xfoil_runner(0, 5, 0.5, True, self.results_dir)

        results_file = os.path.join(self.results_dir, "aerofoil_results.txt")
        self.assertTrue(os.path.exists(results_file))

        with open(results_file) as open_file:
            content = open_file.read()

        self.assertEqual(content.replace(" ", ""),
                         self.expected_content.replace(" ", ""),
                         "content in xfoil result is not correct")

    def test_correct_json(self):

        file_path = "/Applications/Xfoil.app/Contents/Resources/xfoil"

        os.makedirs(self.results_dir)

        xfoil_runner = XfoilRunner(file_path)
        xfoil_runner.setup_analysis(self.aerofoil_file, 1e6)
        results = xfoil_runner(0, 5, 0.5, True, self.results_dir)

        results_file = os.path.join(self.results_dir, "aerofoil_results.txt")
        self.assertTrue(os.path.exists(results_file))

        xfoil_dict = self.expected_json["xfoil"]

        self.assertEqual(results._results_dict, self.expected_json )

if __name__ == "__main__":
    unittest.main()
