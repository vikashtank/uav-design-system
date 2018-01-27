from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.optimisation as opt

class TestCase(unittest.TestCase):

    def setUp(self):
        self.input_dict = {
                            "name1": {
                                        "max": 5,
                                        "min": 4
                                     },
                            "name2": {
                                        "max": 7,
                                        "min": 2
                                     }
                           }
        self.schema = opt.Schema.from_dict(self.input_dict)
        self.Genetic = opt.Genetic(opt.GeneticFactory(), self.schema)

    def test_create_random_dict(self):
        """
        tests a random dict is created within schema constraints
        """
        actual_dict = self.Genetic._create_random_dict()
        self.assertTrue("name1" in actual_dict)
        self.assertTrue("name2" in actual_dict)
        self.assertTrue(4 < actual_dict["name1"] < 5)
        self.assertTrue(2 < actual_dict["name2"] < 7)



if __name__ == "__main__":
    unittest.main()
