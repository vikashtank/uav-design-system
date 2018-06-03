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
        try:
            shutil.rmtree(self.results_dir)
        except FileNotFoundError:
            pass

        # read the results file that is expected to be produced
        self.aerofoil_file = os.path.join(this_directory, 'resources', 'test_aerofoil.txt')
        self.expected_content = get_resource_content('aerofoil_results.txt')
        comparison_json = os.path.join(this_directory, 'resources', 'expected_results.json')
        with open(comparison_json) as open_file:
            self.expected_json = json.load(open_file)

        file_path = '/Applications/Xfoil.app/Contents/Resources/xfoil'
        os.makedirs(self.results_dir)
        self.xfoil_runner = XfoilRunner(file_path)

    def tearDown(self):
        shutil.rmtree(self.results_dir)

    def test_temp_file_location(self):
        temp_folder = Path.home() / 'xfoil_temp'
        self.assertTrue(temp_folder.exists())

    def test_del(self):
        file_location = self.xfoil_runner.temp_folder
        del self.xfoil_runner
        self.assertFalse(file_location.exists())

    def test_run_success(self):

        results = self.xfoil_runner(self.aerofoil_file, 1e6, 0, 5, 0.5, True, self.results_dir)

        results_file = os.path.join(self.results_dir, 'aerofoil_results.txt')
        self.assertTrue(os.path.exists(results_file))

        with open(results_file) as open_file:
            content = open_file.read()
        self.maxDiff = None
        self.assertEqual(content.replace(' ', ''),
                         self.expected_content.replace(' ', ''),
                         'content in xfoil result is not correct')

    def test_correct_json(self):

        results = self.xfoil_runner(self.aerofoil_file, 1e6, 0, 5, 0.5, True, self.results_dir)

        results_file = os.path.join(self.results_dir, 'aerofoil_results.txt')
        self.assertTrue(os.path.exists(results_file))

        xfoil_dict = self.expected_json['xfoil']
        self.maxDiff = None
        self.assertEqual(results._results_dict, self.expected_json )

    def _test_(self):
        aerofoil_file = os.path.join(this_directory, 'resources', 'test_aerofoil2.txt')
        self.xfoil_runner.setup_analysis(aerofoil_file, 67952)
        results = self.xfoil_runner(-1, 1, 0.5, True, self.results_dir)

if __name__ == "__main__":
    unittest.main()
