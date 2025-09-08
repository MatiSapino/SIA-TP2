import random

import numpy as np

from src.models.individual import Individual


class Crossover:

    def __init__(self, chosen_parents, children_size, amount_of_triangle):
        self.chosen_parents = chosen_parents
        self.children_size = children_size
        self.amount_of_triangle = amount_of_triangle

    def one_point(self):
        new_population = []

        while len(new_population) < self.children_size:
            parent1, parent2 = random.sample(self.chosen_parents, 2)
            triangles1 = parent1.get_triangles()
            triangles2 = parent2.get_triangles()

            locus = random.randint(0, self.amount_of_triangle - 1)

            child_triangles1 = np.concatenate([triangles1[:locus], triangles2[locus:]])
            child_triangles2 = np.concatenate([triangles2[:locus], triangles1[locus:]])

            child1 = Individual.from_triangles(child_triangles1)
            child2 = Individual.from_triangles(child_triangles2)

            new_population.extend([child1, child2])

        return new_population[:self.children_size]

    def two_point(self):
        new_population = []

        while len(new_population) < self.children_size:
            parent1, parent2 = random.sample(self.chosen_parents, 2)
            triangles1 = parent1.get_triangles()
            triangles2 = parent2.get_triangles()

            p1, p2 = sorted(random.sample(range(0, self.amount_of_triangle), 2))

            child_triangles1 = np.concatenate([
                triangles1[:p1],
                triangles2[p1:p2],
                triangles1[p2:]
            ])
            child_triangles2 = np.concatenate([
                triangles2[:p1],
                triangles1[p1:p2],
                triangles2[p2:]
            ])

            child1 = Individual.from_triangles(child_triangles1)
            child2 = Individual.from_triangles(child_triangles2)

            new_population.extend([child1, child2])

        return new_population[:self.children_size]

    def annular(self):
        new_population = []

        while len(new_population) < self.children_size:
            parent1, parent2 = random.sample(self.chosen_parents, 2)
            triangles1 = parent1.get_triangles()
            triangles2 = parent2.get_triangles()

            size = self.amount_of_triangle

            locus_p = random.randint(0, size - 1)
            size_l = random.randint(0, (size + 1) // 2)

            mask = np.zeros(size, dtype=bool)
            for i in range(size_l):
                mask[(locus_p + i) % size] = True

            child_triangles1 = np.where(mask, triangles2, triangles1)
            child_triangles2 = np.where(mask, triangles1, triangles2)

            child1 = Individual.from_triangles(child_triangles1)
            child2 = Individual.from_triangles(child_triangles2)

            new_population.extend([child1, child2])

        return new_population[:self.children_size]

    def uniform(self, p):
        new_population = []

        while len(new_population) < self.children_size:
            parent1, parent2 = random.sample(self.chosen_parents, 2)
            triangles1 = parent1.get_triangles()
            triangles2 = parent2.get_triangles()

            mask = np.random.rand(self.amount_of_triangle) < p

            child_triangles1 = np.where(mask[:, None], triangles1, triangles2)
            child_triangles2 = np.where(mask[:, None], triangles2, triangles1)

            child1 = Individual.from_triangles(child_triangles1)
            child2 = Individual.from_triangles(child_triangles2)

            new_population.extend([child1, child2])

        return new_population[:self.children_size]