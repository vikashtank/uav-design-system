"""
file for construting the genetic algorithm for use in this project
"""
from abc import ABC, abstractmethod
from .schema import Schema
import random


class Child():

    def __init__(self, inputs):
        self.inputs = inputs
        self.child = None
        self.results = None


class GeneticFactory(ABC):
    pass


class Genetic(ABC):


    def __init__(self, factory: GeneticFactory, schema: Schema):
        self.factory = factory
        self.schema = schema

    def fitness(self):
        pass

    def generate_population(self, population_size):
        """
        generate many potential designs for the initial run
        """
        population = []

        while(len(population) < population_size):
            child = create_random_child()
            if self.is_valid_child(child):
                population.append(child)

        return population

    def analyse(self, child: Child):
        pass

    def _mutate(self, kwargs):
        """
        mutate the kwarg dictionary according to schema
        """
        new_dict = {}
        for key, value in kwargs.items():
            constraint = self.schema[key]
            delta = 0.01 * (constraint.max - constraint.min)
            sign = random.choice([1, -1])
            new_dict[key] = value + sign * delta
        return new_dict


    def run_genetic(self, generations = 10, store = False, display = False):

        for child in generate_population():
            child.results = self.analyse(child)
            fitness = self.fitness(child.results)

    def _combine(self, dict1, dict2):
        """
        takes two children, and combines their input dictionaries to create
        a new child
        """
        dict3 = {}
        for index, key in enumerate(dict1):
            if index%2 == 0:
                dict3[key] = dict1[key]
            else:
                dict3[key] = dict2[key]
        return dict3

    def create_random_child(self, kwargs):
        # create a child dictionary from schema
        new_child_dict = self._create_random_dict()

    def _create_random_dict(self):
        """
        creates a random dictionary within the schema constraints
        """
        new_child_dict = {}
        for constraint in self.schema:
            val = random.uniform(constraint.min, constraint.max)
            val = round(val, 4)
            new_child_dict[constraint.name] = val
        return new_child_dict


class GeneticInterface(ABC):

    def __init__(self, schema = None):
        self.schema = schema

    @abstractmethod
    def _check_against_schema(self, input_dict):
        pass

    @abstractmethod
    def analyse(self, surface):
        pass

    def _check_input_dict_keys(self, input_dict):

        for key in self.schema:
            try:
                inut_dict[key]
            except AttributeError:
                pass



















if __name__ == "__main__":
    pass
