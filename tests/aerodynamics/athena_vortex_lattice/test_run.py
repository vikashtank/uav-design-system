from os.path import join, exists, dirname, abspath
from os import makedirs
from pathlib import Path
import sys
import unittest
import shutil

this_directory = Path(dirname(abspath(__file__)))
sys.path.append(str(this_directory) + '/../../../')  # so uggo thanks to atom runner
from uav_design_system.aerodynamics.athena_vortex_lattice import AVLRunner, AVLResults


resources_folder = this_directory / 'resources' / 'run_resources'

class CustomAssertions():

    def read_file(self, file):
        with open(str(file)) as open_file:
            return open_file.read()

    def assertFilesSame(self, file1, file2):
        """
        tests that the content of two files are the same
        """
        file1_content = self.read_file(file1)
        file2_content = self.read_file(file2)

        if file1_content != file2_content:
            raise AssertionError('{0} is not the same as {1}'.format(file1,
                                                                     file2))

    def assertPathExists(self, path_object):
        self.assertTrue(path_object.exists())

class TestRun(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.results_dir = this_directory / 'results_dir'
        try:
            shutil.rmtree(self.results_dir)
        except FileNotFoundError:
            pass
        makedirs(self.results_dir)

        self.geom_file = resources_folder / 'allegro.avl'
        self.mass_file = resources_folder / 'allegro.mass'
        self.config_file = resources_folder / 'bd2.run'

        avl_runner = AVLRunner()
        avl_runner.setup_analysis(str(self.geom_file),
                                  str(self.mass_file),
                                  str(self.config_file))
        self.results = avl_runner.generate_results(str(self.results_dir))

    def tearDown(self):
        shutil.rmtree(str(self.results_dir))

    def test_run_create_files(self):
        """
        uses files in resources to test if avl is generating the correct files
        """
        self.assertPathExists(self.results_dir / 'ft.txt')
        self.assertPathExists(self.results_dir / 'hm.txt')
        self.assertPathExists(self.results_dir / 'st.txt')
        self.assertPathExists(self.results_dir / 'fn.txt')
        self.assertPathExists(self.results_dir / 'fs.txt')
        self.assertPathExists(self.results_dir / 'vm.txt')

    def test_run_correct_file_content(self):
        """
        checks the files created by AVL running contain the correct content,
        when compared to the manual runs
        """
        # get expected files
        expected_ft = resources_folder / 'ft.txt'
        expected_hm = resources_folder / 'hm.txt'
        expected_st = resources_folder / 'st.txt'

        # get actual files
        actual_ft = self.results_dir / 'ft.txt'
        actual_hm = self.results_dir / 'hm.txt'
        actual_st = self.results_dir / 'st.txt'

        # check files are the same
        self.assertFilesSame(expected_ft, actual_ft)
        self.assertFilesSame(expected_hm, actual_hm)
        self.assertFilesSame(expected_st, actual_st)

    def test_run_correct_output(self):

        # get actual files
        actual_ft = self.results_dir / 'ft.txt'
        actual_hm = self.results_dir / 'hm.txt'
        actual_st = self.results_dir / 'st.txt'

        self.assertTrue(isinstance(self.results, AVLResults))
        self.assertEqual(self.read_file(actual_ft), self.results._total_forces)
        self.assertEqual(self.read_file(actual_hm), self.results._hinge_forces)
        self.assertEqual(self.read_file(actual_st), self.results._stability_forces)

    def test_run_failure(self):
        pass

if __name__ == "__main__":
    unittest.main()
