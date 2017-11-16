import os
this_directory = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(this_directory + "/../")
import unittest
from run import AVLRunner
import shutil




class Test(unittest.TestCase):


    def setUp(self):
        self.results_dir = os.path.join(this_directory, "results_dir")
        try:
            shutil.rmtree(self.results_dir)
        except FileNotFoundError:
            pass


    def test_run_success(self):

        file_path = os.path.join(this_directory, "../avl3.35")
        geom_file = os.path.join(this_directory, "resources", "allegro.avl")
        mass_file = os.path.join(this_directory, "resources", "allegro.mass")
        config_file = os.path.join(this_directory, "resources", "bd2.run")

        os.makedirs(self.results_dir)

        avl_runner = AVLRunner(file_path)
        avl_runner.setup_analysis( geom_file, mass_file, config_file, [])
        results_dict = avl_runner.generate_results( True, self.results_dir)

        self.assertTrue(os.path.exists(os.path.join(self.results_dir, "ft.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.results_dir, "hm.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.results_dir, "st.txt")))

        shutil.rmtree(self.results_dir)



if __name__ == "__main__":
    unittest.main()
