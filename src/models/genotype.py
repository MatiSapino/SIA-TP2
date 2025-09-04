import numpy as np


class Genotype:

    def __init__(self):
        self.gen_color: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.gen_triangle: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] = ((0, 0), (0, 0), (0, 0))

    def chromosome(self):
        flat_triangle = tuple(coordinate for point in self.gen_triangle for coordinate in point)
        return np.array(self.gen_color + flat_triangle)

    @classmethod
    def from_chromosome(cls, chromosome):
        individual = cls()
        individual.gen_color = (
            int(chromosome[0]),
            int(chromosome[1]),
            int(chromosome[2]),
            int(chromosome[3])
        )
        individual.gen_triangle = (
            (int(chromosome[4]), int(chromosome[5])),
            (int(chromosome[6]), int(chromosome[7])),
            (int(chromosome[8]), int(chromosome[9])),
        )
        return individual