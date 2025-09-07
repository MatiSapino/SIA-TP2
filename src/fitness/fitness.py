import numpy as np
import cv2

from src.models.individual import Individual


class Fitness:

    def __init__(self, population, target_image):
        self.population = population
        self.target_image = target_image

    def fitness(self, individual: Individual):
        generated = self.render_individual(individual)
        error = float(np.mean((self.target_image - generated) ** 2))
        fitness = 1 / (1 + error)
        individual.update_fitness(fitness)
        return fitness

    def relative_fitness(self, individual):
        total_fitness = sum(self.fitness(ind) for ind in self.population)
        relative_fitness = self.fitness(individual) /total_fitness
        individual.update_relative_fitness(relative_fitness)
        return relative_fitness

    def render_individual(self, individual):
        canvas = np.ones_like(self.target_image, dtype=np.uint8) * 255

        for triangle in individual.get_triangles():
            r, g, b, a = triangle.gen_color
            alpha = a / 255

            points = np.array(triangle.gen_triangle, np.int32).reshape((-1, 1, 2))

            triangle_layer = canvas.copy()
            cv2.fillPoly(triangle_layer, [points], (r, g, b))

            canvas = cv2.addWeighted(triangle_layer, alpha, canvas, 1 - alpha, 0)

        return canvas