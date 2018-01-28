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


class Genetic():


    def __init__(self, factory: GeneticFactory, schema: Schema):
        self.factory = factory
        self.schema = schema

    def fitness(self):
        pass

    def generate_initial_population(self, population_size):
        """
        generate many potential designs for the initial run
        """
        population = []

        while(len(population) < population_size):
            child = self._create_random_child()
            if self.is_valid_child(child):
                population.append(child)

        return population

    def analyse(self, child: Child):
        pass

    def is_valid_child(self, child):
        """
        checks the child created
        """
        return True

    def filter_population(self, children):
        """
        filters the population on how well they perform
        """
        half_size = int(0.5 * len(children))
        best_children = children[0: half_size]
        return best_children

    def _mutate(self, kwargs):
        """
        mutate the kwarg dictionary according to schema
        """
        new_dict = {}
        for key, value in kwargs.items():
            constraint = self.schema[key]
            delta = 0.01 * (constraint.max - constraint.min)
            sign = random.choice([1, -1])
            new_value = value + sign * delta
            #enforce schema constraints
            new_dict[key] = self._confine(new_value, constraint.min, constraint.max)
        return new_dict

    def _confine(self, value, min, max):
        if value < min:
            value = min
        elif value > max:
            value = max
        return value

    def run_genetic(self, initial_population, current_generation, max_generations):
        """
        takes an intial population and returns
        """
        children = initial_population

        if current_generation < max_generations - 1:
            best_children = self.filter_population(initial_population)
            next_population = self.generate_next_population(best_children)
            children = children + self.run_genetic(next_population,
                                                   current_generation + 1,
                                                   max_generations)

        return children

    def generate_next_population(self, population):
        """
        create a new population from the filtered population
        """
        return population * 2

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

    def child_from_parents(self, parent1, parent2):
        """
        create a child from two parents and mutate the child to produce
        next generation

        inputs
            parent1(dict[str, foat]): a dictionary of strings to floats
            parent2(dict[str, foat]): a dictionary of strings to floats
        """
        combined_dict = self._combine(parent1, parent2)
        return self.mutate(combined_dict)

    def _create_random_child(self):
        """
        creates a random dictionary within the schema constraints
        """
        new_child_dict = {}
        for constraint in self.schema:
            val = random.uniform(constraint.min, constraint.max)
            val = round(val, 4)
            new_child_dict[constraint.name] = val
        return new_child_dict

    def __call__(self, generations = 10, store = False, display = False):
        initial_population = self.generate_initial_population(generations)
        return self.run_genetic(initial_population, 0, generations)


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
