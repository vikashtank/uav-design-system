from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system.aerodynamics.athena_vortex_lattice import AVLRunner, AVLResults
import shutil

class CustomAssertions():

    def _read_file(self, file):
        with open(file) as open_file:
            return open_file.read()

    def assertFilesSame(self, file1: str, file2: str):
        """
        tests that the content of two files are the same
        """
        file1_content = self._read_file(file1)
        file2_content = self._read_file(file2)

        if file1_content != file2_content:
            raise AssertionError("{0} is not the same as {1}".format(file1,
                                                                     file2))

class TestRun(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.results_dir = join(this_directory, "results_dir")
        try:
            shutil.rmtree(self.results_dir)
        except FileNotFoundError:
            pass
        makedirs(self.results_dir)

        self.resources_folder = join(this_directory, "resources")
        self.geom_file = join(self.resources_folder, "allegro.avl")
        self.mass_file = join(self.resources_folder, "allegro.mass")
        self.config_file = join(self.resources_folder, "bd2.run")

        avl_runner = AVLRunner()
        avl_runner.setup_analysis(self.geom_file,
                                  self.mass_file,
                                  self.config_file)
        self.results = avl_runner.generate_results(self.results_dir)

    def tearDown(self):
        shutil.rmtree(self.results_dir)

    def test_run_create_files(self):
        """
        uses files in resources to test if avl is generating the correct files
        """

        self.assertTrue(exists(join(self.results_dir, "ft.txt")))
        self.assertTrue(exists(join(self.results_dir, "hm.txt")))
        self.assertTrue(exists(join(self.results_dir, "st.txt")))
        self.assertTrue(exists(join(self.results_dir, "fn.txt")))
        self.assertTrue(exists(join(self.results_dir, "fs.txt")))
        self.assertTrue(exists(join(self.results_dir, "vm.txt")))

    def test_run_correct_file_content(self):
        """
        checks the files created by AVL running contain the correct content,
        when compared to the manual runs
        """
        # get expected files
        expected_ft = join(self.resources_folder, "ft.txt")
        expected_hm = join(self.resources_folder, "hm.txt")
        expected_st = join(self.resources_folder, "st.txt")

        # get actual files
        actual_ft = join(self.results_dir, "ft.txt")
        actual_hm = join(self.results_dir, "hm.txt")
        actual_st = join(self.results_dir, "st.txt")

        # check files are the same
        self.assertFilesSame(expected_ft, actual_ft)
        self.assertFilesSame(expected_hm, actual_hm)
        self.assertFilesSame(expected_st, actual_st)

    def test_run_correct_output(self):

        # get actual files
        actual_ft = join(self.results_dir, "ft.txt")
        actual_hm = join(self.results_dir, "hm.txt")
        actual_st = join(self.results_dir, "st.txt")

        self.assertTrue(isinstance(self.results, AVLResults))
        self.assertEqual(self._read_file(actual_ft), self.results._total_forces)
        self.assertEqual(self._read_file(actual_hm), self.results._hinge_forces)
        self.assertEqual(self._read_file(actual_st), self.results._stability_forces)




if __name__ == "__main__":
    unittest.main()
