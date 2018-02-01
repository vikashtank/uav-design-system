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
        self.test_dict_small = {
                                "name1": 4.5,
                                "name2": 4,
                                }
        self.schema = opt.Schema.from_dict(self.input_dict)
        self.genetic = opt.Genetic(opt.GeneticFactory(), self.schema)

    def test_create_random_child(self):
        """
        tests a random dict is created within schema constraints
        """
        child = self.genetic._create_random_child()
        self.assertIsInstance(child, opt.Child)
        actual_dict = child.inputs
        self.assertTrue("name1" in actual_dict)
        self.assertTrue("name2" in actual_dict)
        self.assertTrue(4 < actual_dict["name1"] < 5)
        self.assertTrue(2 < actual_dict["name2"] < 7)

    def test_create_initial_population(self):
        population = self.genetic.generate_initial_population(10)
        self.assertEqual(len(population), 10)
        for i in population:
            self.assertIsInstance(i, opt.Child)


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
        actual_dict = self.genetic._mutate(self.test_dict_small)
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

    def test_run(self):
        children = self.genetic()
        self.assertEqual(len(children), 100)

    def test_generate_next_population(self):
        initial_population = []
        for i in range(5):
            child = opt.Child(self.test_dict_small)
            initial_population.append(child)

        new_population = self.genetic.generate_next_population(initial_population)
        self.assertEqual(len(new_population), 10)

class TestChild(unittest.TestCase):

    def setUp(self):
        self.input_dict = {"inputs": 1}
        self.child_instance = opt.Child(self.input_dict)

    def tearDown(self):
        pass

    def test_results_property(self):

        self.child_instance.results = "hello"
        self.assertEqual(self.child_instance.results, "hello")

    def test_inputs_property(self):

        self.assertEqual(self.child_instance.inputs, self.input_dict)




if __name__ == "__main__":
    unittest.main()
