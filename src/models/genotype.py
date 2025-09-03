import numpy as np


class Genotype:

    def __init__(self):
        self.gen_color: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.gen_triangle: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] = ((0, 0), (0, 0), (0, 0))

    def chromosome(self):
        flat_triangle = tuple(coordinate for point in self.gen_triangle for coordinate in point)
        return np.array(self.gen_color + flat_triangle)