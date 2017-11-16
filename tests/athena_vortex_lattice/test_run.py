from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system.athena_vortex_lattice import AVLRunner
import shutil


class Test(unittest.TestCase):


    def setUp(self):
        self.results_dir = join(this_directory, "results_dir")
        try:
            shutil.rmtree(self.results_dir)
        except FileNotFoundError:
            pass

    def tearDown(self):
        shutil.rmtree(self.results_dir)

    def test_run_success(self):

        geom_file = join(this_directory, "resources", "allegro.avl")
        mass_file = join(this_directory, "resources", "allegro.mass")
        config_file = join(this_directory, "resources", "bd2.run")

        makedirs(self.results_dir)

        avl_runner = AVLRunner()
        avl_runner.setup_analysis( geom_file, mass_file, config_file)
        results_dict = avl_runner.generate_results(self.results_dir)

        self.assertTrue(exists(join(self.results_dir, "ft.txt")))
        self.assertTrue(exists(join(self.results_dir, "hm.txt")))
        self.assertTrue(exists(join(self.results_dir, "st.txt")))





if __name__ == "__main__":
    unittest.main()
