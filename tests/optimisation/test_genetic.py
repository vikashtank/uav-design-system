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
        self.test_dict = {
                            "name1": 0,
                            "name2": 1,
                            "name3": 2,
                            "name4": 3,
                            "name5": 4
                        }
        self.schema = opt.Schema.from_dict(self.input_dict)
        self.genetic = opt.Genetic(opt.GeneticFactory(), self.schema)

    def test_create_random_dict(self):
        """
        tests a random dict is created within schema constraints
        """
        actual_dict = self.genetic._create_random_dict()
        self.assertTrue("name1" in actual_dict)
        self.assertTrue("name2" in actual_dict)
        self.assertTrue(4 < actual_dict["name1"] < 5)
        self.assertTrue(2 < actual_dict["name2"] < 7)

    def test_combine(self):

        test_dict2 = {
                        "name1": 5,
                        "name2": 6,
                        "name3": 7,
                        "name4": 8,
                        "name5": 9
                    }
        new_dict = self.genetic._combine(self.test_dict, test_dict2)
        self.assertEqual(new_dict, {"name1": 0,
                                    "name2": 6,
                                    "name3": 2,
                                    "name4": 8,
                                    "name5": 4
                                    })

    def test_mutate(self):
        test_dict = {
                        "name1": 4.5,
                        "name2": 4,
                    }
        actual_dict = self.genetic._mutate(test_dict)
        self.assertTrue("name1" in actual_dict)
        self.assertTrue("name2" in actual_dict)
        self.assertTrue(4 < actual_dict["name1"] < 5)
        self.assertTrue(2 < actual_dict["name2"] < 7)
        self.assertTrue(actual_dict["name1"] != 4.5)
        self.assertTrue(actual_dict["name2"] != 4)

    def test_confine(self):
        self.assertEqual(self.genetic._confine(5, 4, 6), 5)
        self.assertEqual(self.genetic._confine(4, 4, 6), 4)
        self.assertEqual(self.genetic._confine(6, 4, 6), 6)
        self.assertEqual(self.genetic._confine(3, 4, 6), 4)
        self.assertEqual(self.genetic._confine(7, 4, 6), 6)





if __name__ == "__main__":
    unittest.main()
