

class SchemaComparisonError(Exception):
    pass

class Constraint():

    def __init__(self, name, min, max):
        self.name = name
        self.min = min
        self.max = max

    def __call__(self, value):
        return self.min < value < self.max

    def __eq__(self, value: "Constraint"):

        return self.name == value.name and self.min == value.min and self.max == value.max

class Schema():
    """
    class used for testing dictionary values,
    ensure that dictionaries are the correct size and have values within
    the correct range in the schema
    """

    def __init__(self, *constraints: Constraint):

        if not constraints:
            self._constraints = []
        else:
            self._constraints = List(constraints)

    @property
    def constraint_names(self):
        return [x.name for x in self._constraints]

    def append(self, value: "Constraint"):
        self._constraints.append(value)

    def __call__(self, dict):
        """
        compares dict against schema
        """
        self._compare_size(dict)
        self._compare_keys(dict)
        self._compare_values(dict)

    def __getitem__(self, key):
        return [x for x in self._constraints if x.name == key][0]

    def _compare_size(self, dict):
        """
        checks the size of the dictionary is correct against the schema
        """
        actual_len = len(dict)
        expected_len = len(self._constraints)
        if actual_len != expected_len:
            raise SchemaComparisonError(f"expected number of values to be"
                                     " {expected_len} but got {actual_len}")

    def _compare_keys(self, dict):
        """
        checks all the keys in dict are inside the schema
        """
        schema_names = self.constraint_names
        for key in dict:
            if key not in schema_names:
                raise SchemaComparisonError(f"no constraint named {key} in schema")

    def _compare_values(self, dict):
        """
        checks all the values of the dict are within tolerances in schema
        """
        for key, value in dict.items():
            constraint = self[key]
            if not constraint(value):
                raise SchemaComparisonError(f"constraint for {key} not satisfied")


    @staticmethod
    def from_dict(dict):
        """
        turns a dictionary into a schema class
        """
        schema = Schema()
        for key in dict:
            max = dict[key]["max"]
            min = dict[key]["min"]
            constraint = Constraint(key, min, max)
            schema.append(constraint)

        return schema
