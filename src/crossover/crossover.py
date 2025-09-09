import math
import random

from src.models.individual import Individual


class Crossover:

    def __init__(self, chosen_parents, children_size, amount_of_triangle, crossover_probability):
        self.chosen_parents = chosen_parents
        self.children_size = children_size
        self.amount_of_triangle = amount_of_triangle
        self.crossover_probability = crossover_probability

    def one_point(self):
        new_population = []

        while len(new_population) < self.children_size:
            parent1, parent2 = random.sample(self.chosen_parents, 2)

            if random.random() < self.crossover_probability:
                triangles1 = parent1.get_triangles()
                triangles2 = parent2.get_triangles()

                locus = random.randint(0, self.amount_of_triangle - 1)

                child_triangles1 = triangles1[:locus] + triangles2[locus:]
                child_triangles2 = triangles2[:locus] + triangles1[locus:]

                child1 = Individual.from_triangles(child_triangles1)
                child2 = Individual.from_triangles(child_triangles2)
            else:
                child1 = parent1
                child2 = parent2

            new_population.extend([child1, child2])

        return new_population[:self.children_size]

    def two_point(self):
        new_population = []

        while len(new_population) < self.children_size:
            parent1, parent2 = random.sample(self.chosen_parents, 2)

            if random.random() < self.crossover_probability:
                triangles1 = parent1.get_triangles()
                triangles2 = parent2.get_triangles()

                p1, p2 = sorted(random.sample(range(0, self.amount_of_triangle), 2))

                child_triangles1 = triangles1[:p1] + triangles2[p1:p2] + triangles1[p2:]
                child_triangles2 = triangles2[:p1] + triangles1[p1:p2] + triangles2[p2:]

                child1 = Individual.from_triangles(child_triangles1)
                child2 = Individual.from_triangles(child_triangles2)
            else:
                child1 = parent1
                child2 = parent2

            new_population.extend([child1, child2])

        return new_population[:self.children_size]

    def annular(self):
        new_population = []

        while len(new_population) < self.children_size:
            parent1, parent2 = random.sample(self.chosen_parents, 2)

            if random.random() < self.crossover_probability:
                triangles1 = parent1.get_triangles()
                triangles2 = parent2.get_triangles()

                size = self.amount_of_triangle

                locus_p = random.randint(0, size - 1)
                size_l = random.randint(0, math.ceil(size / 2))

                child_triangles1 = []
                child_triangles2 = []

                for i in range(size):
                    is_in_annulus = ((i - locus_p + size) % size) < size_l
                    if is_in_annulus:
                        child_triangles1.append(triangles2[i])
                        child_triangles2.append(triangles1[i])
                    else:
                        child_triangles1.append(triangles1[i])
                        child_triangles2.append(triangles2[i])

                child1 = Individual.from_triangles(child_triangles1)
                child2 = Individual.from_triangles(child_triangles2)
            else:
                child1 = parent1
                child2 = parent2

            new_population.extend([child1, child2])

        return new_population[:self.children_size]

    def uniform(self, p):
        new_population = []

        while len(new_population) < self.children_size:
            parent1, parent2 = random.sample(self.chosen_parents, 2)

            if random.random() < self.crossover_probability:
                triangles1 = parent1.get_triangles()
                triangles2 = parent2.get_triangles()

                child_triangles1 = []
                child_triangles2 = []

                for i in range(self.amount_of_triangle):
                    if random.random() < p:
                        child_triangles1.append(triangles1[i])
                        child_triangles2.append(triangles2[i])
                    else:
                        child_triangles1.append(triangles2[i])
                        child_triangles2.append(triangles1[i])

                child1 = Individual.from_triangles(child_triangles1)
                child2 = Individual.from_triangles(child_triangles2)
            else:
                child1 = parent1
                child2 = parent2

            new_population.extend([child1, child2])

        return new_population[:self.children_size]