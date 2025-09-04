import random

import numpy as np

from src.models.genotype import Genotype


class Crossover:

    def __init__(self, selected_population, new_population_size):
        self.selected_population = selected_population
        self.new_population_size = new_population_size

    def one_point(self):
        new_population = []

        while len(new_population) < self.new_population_size:
            parent1, parent2 = random.sample(self.selected_population, 2)
            chromosome1 = parent1.chromosome()
            chromosome2 = parent2.chromosome()

            locus = random.randint(1, len(chromosome1) - 1)

            child_chromosome1 = np.concatenate([chromosome1[:locus], chromosome2[locus:]])
            child_chromosome2 = np.concatenate([chromosome2[:locus], chromosome1[locus:]])

            child1 = Genotype.from_chromosome(child_chromosome1)
            child2 = Genotype.from_chromosome(child_chromosome2)

            new_population.extend([child1, child2])

        return new_population[:self.new_population_size]