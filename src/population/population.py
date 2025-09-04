import random

from src.models.genotype import Genotype


def generate_initial_population(target_image, population_size):
    height, width, channels = target_image.shape
    population = []

    for _ in range(population_size):
        individual = Genotype()

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        a = random.randint(0, 255)
        individual.gen_color = (r, g, b, a)

        while True:
            triangle = [
                (random.randint(0, width - 1), random.randint(0, height - 1)),
                (random.randint(0, width - 1), random.randint(0, height - 1)),
                (random.randint(0, width - 1), random.randint(0, height - 1)),
            ]

            if len(set(triangle)) == 3:
                break

        p1, p2, p3 = triangle
        individual.gen_triangle = (p1, p2, p3)

        population.append(individual)

    return population