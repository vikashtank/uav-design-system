import os
from os.path import join
this_directory = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(this_directory + '/../../../')
import unittest
from uav_design_system.aerodynamics.xfoil import XfoilRunner
import shutil
import json
from pathlib import Path

def get_resource_content(file_name):
    """
    function to retrieve data from files in the resource folder for these tests
    """
    resources_directory = join(this_directory, 'resources')
    with open(join(resources_directory, file_name)) as open_file:
        return open_file.read()

class TestXfoilRunner(unittest.TestCase):

    def setUp(self):
        self.results_dir = os.path.join(this_directory, 'results_dir')

        # read the results file that is expected to be produced
        self.aerofoil_file = os.path.join(this_directory, 'resources', 'test_aerofoil.txt')

        file_path = '/Applications/Xfoil.app/Contents/Resources/xfoil'
        self.xfoil_runner = XfoilRunner(file_path)

    def tearDown(self):
        pass

    def test_temp_file_location(self):
        temp_folder = Path.home() / 'xfoil_temp'
        self.assertTrue(temp_folder.exists())

    def test_del(self):
        file_location = self.xfoil_runner.temp_folder
        del self.xfoil_runner
        self.assertFalse(file_location.exists())

    def test_run_success_output_file(self):
        results_dir = os.path.join(this_directory, 'results_dir')
        os.makedirs(self.results_dir)
        results = self.xfoil_runner(self.aerofoil_file, 1e6, 0, 5, 0.5, self.results_dir)
        results_file = os.path.join(results_dir, 'aerofoil_results.txt')

        with open(results_file) as open_file:
            content = open_file.read()

        self.maxDiff = None
        expected_content = get_resource_content('aerofoil_results.txt')
        self.assertEqual(content.replace(' ', ''),
                         expected_content.replace(' ', ''),
                         'content in xfoil result is not correct')

        shutil.rmtree(self.results_dir)

    def test_run_success_output(self):
        comparison_json = os.path.join(this_directory, 'resources', 'expected_results.json')
        with open(comparison_json) as open_file:
            expected_json = json.load(open_file)
        results = self.xfoil_runner(self.aerofoil_file, 1e6, 0, 5, 0.5)

        xfoil_dict = expected_json['xfoil']
        self.maxDiff = None
        comparison_json = os.path.join(this_directory, 'resources', 'expected_results.json')
        self.assertEqual(results._results_dict, expected_json )


if __name__ == "__main__":
    unittest.main()
