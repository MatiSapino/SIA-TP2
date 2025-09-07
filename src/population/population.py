import random

from src.models.genotype import Genotype
from src.models.individual import Individual


def generate_initial_population(target_image, population_size, amount_of_triangle):
    height, width, channels = target_image.shape
    population = []

    for _ in range(population_size):
        individual = Individual()

        for _ in range(amount_of_triangle):
            triangle = Genotype()
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            a = random.randint(0, 255)
            triangle.gen_color = (r, g, b, a)

            while True:
                triangle_points = [
                    (random.randint(0, width - 1), random.randint(0, height - 1)),
                    (random.randint(0, width - 1), random.randint(0, height - 1)),
                    (random.randint(0, width - 1), random.randint(0, height - 1)),
                ]

                if len(set(triangle_points)) == 3:
                    break

            p1, p2, p3 = triangle_points
            triangle.gen_triangle = (p1, p2, p3)

            individual.add_triangle(triangle)

        population.append(individual)

    return population