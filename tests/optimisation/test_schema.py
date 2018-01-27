from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.optimisation as opt

class TestSchema(unittest.TestCase):

    def setUp(self):
        self.schema = opt.Schema()
        self.constraint_1 = opt.Constraint("name1", 4, 5)
        self.constraint_2 = opt.Constraint("name2", 2, 7)
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
                            "name1": 4.5,
                            "name2": 4
                         }

    def test_append(self):

        self.assertEqual(len(self.schema._constraints), 0)
        self.schema.append(self.constraint_1)
        self.assertEqual(self.schema._constraints[0], self.constraint_1)

    def test_from_dict(self):

        schema = opt.Schema.from_dict(self.input_dict)
        self.assertEqual(schema._constraints[0], self.constraint_1)
        self.assertEqual(schema._constraints[1], self.constraint_2)

    def test_call_pass(self):

        self.schema.append(self.constraint_1)
        self.schema.append(self.constraint_2)
        self.schema(self.test_dict)


    def test_call_pass_fail_range(self):

        self.schema.append(self.constraint_1)
        self.schema.append(self.constraint_2)
        self.test_dict["name1"] = 3.9
        with self.assertRaises(opt.SchemaComparisonError):
            self.schema(self.test_dict)

    def test_call_pass_fail_existance(self):

        self.schema.append(self.constraint_1)
        self.schema.append(self.constraint_2)
        self.test_dict = {
                            "name0": 4.5,
                            "name3": 4
                         }
        with self.assertRaises(opt.SchemaComparisonError):
            self.schema(self.test_dict)

    def test_iter(self):
        self.schema.append(self.constraint_1)
        self.schema.append(self.constraint_2)
        constraint_list = [self.constraint_1, self.constraint_2]

        for index, value in enumerate(self.schema):
            self.assertEqual(value, constraint_list[index])


class TestConstraint(unittest.TestCase):

    def setUp(self):
        self.constraint = opt.Constraint("constraint", 0, 4)

    def test_call(self):
        self.assertTrue(self.constraint(0.01))
        self.assertTrue(self.constraint(3.99))
        self.assertTrue(self.constraint(2))

    def test_call_false(self):

        self.assertFalse(self.constraint(-0.1))
        self.assertFalse(self.constraint(4.1))

    def test_eq(self):
        dummy_constraint = opt.Constraint("constraint", 0, 4)
        self.assertEqual(self.constraint, dummy_constraint)

if __name__ == "__main__":
    unittest.main()
