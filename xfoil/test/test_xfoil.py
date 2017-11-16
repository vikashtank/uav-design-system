import os
this_directory = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(this_directory + "/../")
import unittest
from xfoil import XfoilRunner
import shutil


class Test(unittest.TestCase):


    def setUp(self):
        self.results_dir = os.path.join(this_directory, "results_dir")
        try:
            shutil.rmtree(self.results_dir)
        except FileNotFoundError:
            pass

        # read the results file that is expected to be produced
        comparison_file = os.path.join(this_directory, "resources", "aerofoil_results.txt")

        with open(comparison_file) as open_file:
            self.expected_content = open_file.read()


    def test_run_success(self):

        file_path = "/Applications/Xfoil.app/Contents/Resources/xfoil"

        os.makedirs(self.results_dir)

        xfoil_runner = XfoilRunner(file_path)
        xfoil_runner.setup_analysis("0012", 1e6)
        results_dict = xfoil_runner.generate_results(0, 3, 0.5, True, self.results_dir)

        results_file = os.path.join(self.results_dir, "aerofoil_results.txt")
        self.assertTrue(os.path.exists(results_file))

        with open(results_file) as open_file:
            content = open_file.read()

        print(content)
        print("")
        print(self.expected_content)

        self.assertEqual(content.replace(" ", ""),
                        self.expected_content.replace(" ", ""),
                        "content in xfoil result is not correct")

        #shutil.rmtree(self.results_dir)



if __name__ == "__main__":
    unittest.main()
